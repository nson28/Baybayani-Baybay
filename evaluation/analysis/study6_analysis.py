"""Study 6 evaluation analysis (Baybayani MIS and mobile app).

Reads the verified transcription (../Study6_Evaluation_Transcription.md) and writes:
  study6_scores.csv               tidy item responses (one row per respondent x item), codes only
  study6_respondent_summary.csv   per-respondent SUS and Part 2B construct scores
  study6_demographics.csv         coded member profile (R02-R28)
  study6_tables.md                every results table used in the analysis report

Run from any directory:  python evaluation/analysis/study6_analysis.py
Requires Python 3.8+, pandas, numpy, scipy.

Decisions applied (approved by the Component Leader, 2026-11-13):
  * SUS: standard scoring; respondents with <= 2 missing items are prorated
    (mean of answered item contributions x 10 x 2.5); > 2 missing = no score (R14).
  * SUS interpretation: Bangor et al. (2009) adjective (nearest adjective mean) and
    acceptability range; letter grade on the Sauro-Lewis (2016) curved grading scale.
  * Part 2B / 1B (1-7): equal-interval cut-offs of width 6/7 labelled with the form's anchors.
  * Construct score = mean of answered items when at least half the construct is answered
    (PU >= 3 of 5, PEOU >= 3 of 5, BI >= 2 of 3, all 13 items >= 7 of 13); else missing.
  * Item statistics use all available answers; Cronbach's alpha uses complete cases.
"""
from __future__ import annotations

import math
import re
from pathlib import Path

import numpy as np
import pandas as pd
from scipy import stats

HERE = Path(__file__).resolve().parent
SRC = HERE.parent / "Study6_Evaluation_Transcription.md"

SUS_N = 10
B_N = 13
CONSTRUCTS = {  # Part 2B (members) and Part 1B (admin) share this grouping
    "PU": ("Perceived usefulness", list(range(1, 6)), 3),
    "PEOU": ("Perceived ease of use", list(range(6, 11)), 3),
    "BI": ("Intention to use / recommend", list(range(11, 14)), 2),
}
OVERALL_MIN = 7  # of 13

# ---------------------------------------------------------------- scales
SEVEN_POINT = [  # (lower bound, label); equal intervals of width 6/7
    (6.15, "Extremely agree"),
    (5.29, "Agree"),
    (4.43, "Slightly agree"),
    (3.57, "Neutral"),
    (2.72, "Slightly disagree"),
    (1.86, "Disagree"),
    (1.00, "Extremely disagree"),
]

BANGOR_ADJ = [  # Bangor, Kortum & Miller (2009): mean SUS score per adjective
    ("Worst imaginable", 12.5),
    ("Awful", 20.3),
    ("Poor", 35.7),
    ("OK", 50.9),
    ("Good", 71.4),
    ("Excellent", 85.5),
    ("Best imaginable", 90.9),
]

SAURO_LEWIS = [  # Sauro & Lewis (2016) curved grading scale: (lower bound, grade, percentile range)
    (84.1, "A+", "96-100"),
    (80.8, "A", "90-95"),
    (78.9, "A-", "85-89"),
    (77.2, "B+", "80-84"),
    (74.1, "B", "70-79"),
    (72.6, "B-", "65-69"),
    (71.1, "C+", "60-64"),
    (65.0, "C", "41-59"),
    (62.7, "C-", "35-40"),
    (51.7, "D", "15-34"),
    (0.0, "F", "0-14"),
]


def r2(x: float) -> float:
    """Round half away from zero to 2 decimals (avoids banker's rounding in tables)."""
    if x is None or (isinstance(x, float) and math.isnan(x)):
        return float("nan")
    return math.floor(abs(x) * 100 + 0.5) / 100 * (1 if x >= 0 else -1)


def f2(x) -> str:
    return "–" if x is None or (isinstance(x, float) and math.isnan(x)) else f"{r2(x):.2f}"


def seven_label(m: float) -> str:
    m2 = r2(m)
    for lo, lab in SEVEN_POINT:
        if m2 >= lo:
            return lab
    return SEVEN_POINT[-1][1]


def bangor_adjective(score: float) -> str:
    return min(BANGOR_ADJ, key=lambda a: abs(a[1] - score))[0]


def bangor_acceptability(score: float) -> str:
    if score >= 70:
        return "Acceptable"
    if score >= 63:
        return "Marginal (high)"
    if score >= 50:
        return "Marginal (low)"
    return "Not acceptable"


def sl_grade(score: float) -> str:
    s = r2(score)
    for lo, g, _ in SAURO_LEWIS:
        if s >= lo:
            return g
    return "F"


def cronbach_alpha(df: pd.DataFrame) -> tuple[float, int]:
    d = df.dropna()
    k = d.shape[1]
    if len(d) < 3 or k < 2:
        return float("nan"), len(d)
    item_var = d.var(axis=0, ddof=1).sum()
    total_var = d.sum(axis=1).var(ddof=1)
    return k / (k - 1) * (1 - item_var / total_var), len(d)


def describe(s: pd.Series) -> dict:
    s = s.dropna()
    return dict(n=len(s), mean=s.mean(), sd=s.std(ddof=1), median=s.median(), min=s.min(), max=s.max())


# ---------------------------------------------------------------- parsing
LINES = SRC.read_text(encoding="utf-8").splitlines()


def section(start_pat: str, end_pat: str) -> list[str]:
    s = next(i for i, l in enumerate(LINES) if re.match(start_pat, l))
    e = next(i for i in range(s + 1, len(LINES)) if re.match(end_pat, LINES[i]))
    return LINES[s:e]


def cell(x: str):
    x = x.strip()
    if x == "BLANK":
        return None
    if x in ("–", "-"):
        return None
    return int(x)


def code_rows(lines: list[str]) -> dict[str, list]:
    out = {}
    for l in lines:
        m = re.match(r"\| (R\d\d) \|(.*)\|\s*$", l)
        if m:
            out[m.group(1)] = [cell(x) for x in m.group(2).split("|")]
    return out


part2a = code_rows(section(r"### 3\.1 ", r"### 3\.2 "))
part2b = code_rows(section(r"### 3\.2 ", r"## 4\. "))
admin_lines = section(r"## 4\. ", r"## 5\. ")
admin = {}
for l in admin_lines:
    m = re.match(r"\| (1A|1B) \(.*?\) \|(.*)\|\s*$", l)
    if m:
        admin[m.group(1)] = [cell(x) for x in m.group(2).split("|")]
admin["1A"] = admin["1A"][:SUS_N]

assert sorted(part2a) == [f"R{i:02d}" for i in range(2, 29)], "Part 2A rows"
assert sorted(part2b) == [f"R{i:02d}" for i in range(2, 29)], "Part 2B rows"
assert all(len(v) == SUS_N for v in part2a.values()) and all(len(v) == B_N for v in part2b.values())
assert len(admin["1B"]) == B_N


# Cross-check: the summary tables (Sections 3-4) must equal the per-form tables (Section 8).
def per_form_tables() -> dict[str, dict[str, list]]:
    out: dict[str, dict[str, list]] = {}
    sec8 = section(r"## 8\. ", r"## 9\. ")
    code = None
    part = None
    for l in sec8:
        m = re.match(r"### (R\d\d) ", l)
        if m:
            code = m.group(1)
            out[code] = {}
            continue
        m = re.match(r"\*\*Part (1A|1B|2A|2B)", l)
        if m:
            part = m.group(1)
            continue
        if part and re.match(r"\|\s*[0-9B]", l) and not l.startswith("| Q") and not l.startswith("|---"):
            out[code][part] = [cell(x) for x in l.strip().strip("|").split("|")]
            part = None
    return out


pf = per_form_tables()
mismatch = []
for c, v in part2a.items():
    if pf[c].get("2A") != v:
        mismatch.append((c, "2A", pf[c].get("2A"), v))
for c, v in part2b.items():
    if pf[c].get("2B") != v:
        mismatch.append((c, "2B", pf[c].get("2B"), v))
if pf["R01"].get("1A") != admin["1A"]:
    mismatch.append(("R01", "1A", pf["R01"].get("1A"), admin["1A"]))
if pf["R01"].get("1B") != admin["1B"]:
    mismatch.append(("R01", "1B", pf["R01"].get("1B"), admin["1B"]))
for v in list(part2a.values()) + [admin["1A"]]:
    assert all(x is None or 1 <= x <= 5 for x in v), "SUS out of range"
for v in list(part2b.values()) + [admin["1B"]]:
    assert all(x is None or 1 <= x <= 7 for x in v), "1-7 out of range"

# ---------------------------------------------------------------- tidy scores CSV
SUS_ITEMS = [
    "I think I would like to use this application frequently.",
    "I found the application unnecessarily complex.",
    "I thought the application was easy to use.",
    "I think that I need the support of a technical person to be able to use this application.",
    "I found the various functions in the application were well integrated.",
    "I thought there was too much inconsistency in this application.",
    "I would imagine that most people would learn this application very quickly.",
    "I found the application very awkward to use.",
    "I felt very confident in using the application.",
    "I needed to learn a lot of things before I could get going with this application.",
]
B_ITEMS = [
    "Using the application allows me to place orders more quickly.",
    "Using the application makes it more convenient for me to order products from Baybayani.",
    "Using the application helps me keep track of my orders.",
    "Using the application improves my overall online shopping experience.",
    "I find the application useful for buying products from Baybayani.",
    "Learning to use the application was easy for me.",
    "I find it easy to find the products I want.",
    "I find the ordering and checkout process easy to follow.",
    "The user interface of the application is easy to understand.",
    "It is easy for me to become skillful at using the application.",
    "I intend to use the application for my future orders.",
    "I prefer ordering through the application over buying in person.",
    "I would recommend the application to other people.",
]
ADMIN_B_ITEMS = [
    "Using the application helps me record orders more accurately.",
    "Using the application allows me to manage orders more quickly.",
    "Using the application makes retrieving order records easier.",
    "Using the application helps me generate order reports and summaries.",
    "I find the application useful for performing my tasks.",
    "Learning to use the administrator features was easy for me.",
    "I find it easy to view and update order information.",
    "The administrator interface is clear and understandable.",
    "Interacting with the application requires little mental effort.",
    "It is easy for me to get the application to do what I need it to do.",
    "I intend to continue using the application for tracking the organization's orders.",
    "I prefer using the application over my current method of recording orders.",
    "I would recommend the continued use of the application in the organization.",
]


def construct_of(q: int) -> str:
    return next(k for k, (_, items, _) in CONSTRUCTS.items() if q in items)


rows = []
for code, vals in [("R01", admin["1A"])] + sorted(part2a.items()):
    rtype = "Administrator" if code == "R01" else "Member"
    part = "1A" if code == "R01" else "2A"
    for q, v in enumerate(vals, 1):
        rows.append(dict(code=code, respondent_type=rtype, part=part, scale="SUS (1-5)", item=q,
                         construct="SUS-positive" if q % 2 else "SUS-negative", response=v))
for code, vals in [("R01", admin["1B"])] + sorted(part2b.items()):
    rtype = "Administrator" if code == "R01" else "Member"
    part = "1B" if code == "R01" else "2B"
    for q, v in enumerate(vals, 1):
        rows.append(dict(code=code, respondent_type=rtype, part=part, scale="TAM (1-7)", item=q,
                         construct=construct_of(q), response=v))
tidy = pd.DataFrame(rows)
tidy["response"] = tidy["response"].astype("Int64")
tidy.to_csv(HERE / "study6_scores.csv", index=False)

# ---------------------------------------------------------------- SUS
A = pd.DataFrame.from_dict(part2a, orient="index", columns=[f"Q{i}" for i in range(1, 11)]).astype(float)
B = pd.DataFrame.from_dict(part2b, orient="index", columns=[f"Q{i}" for i in range(1, 14)]).astype(float)
A.index.name = B.index.name = "code"


def sus_contrib(df: pd.DataFrame) -> pd.DataFrame:
    c = df.copy()
    for i in range(1, 11):
        c[f"Q{i}"] = (df[f"Q{i}"] - 1) if i % 2 else (5 - df[f"Q{i}"])
    return c


C = sus_contrib(A)
answered = A.notna().sum(axis=1)
sus_prorated = C.mean(axis=1) * 25  # mean contribution x 10 items x 2.5
sus = sus_prorated.where(answered >= SUS_N - 2)
sus_complete = (C.sum(axis=1) * 2.5).where(answered == SUS_N)

admin_c = [(x - 1) if i % 2 == 0 else (5 - x) for i, x in enumerate(admin["1A"])]
admin_sus = sum(admin_c) * 2.5


def construct_scores(df: pd.DataFrame) -> pd.DataFrame:
    out = pd.DataFrame(index=df.index)
    for k, (_, items, need) in CONSTRUCTS.items():
        sub = df[[f"Q{i}" for i in items]]
        out[k] = sub.mean(axis=1).where(sub.notna().sum(axis=1) >= need)
    out["Overall"] = df.mean(axis=1).where(df.notna().sum(axis=1) >= OVERALL_MIN)
    return out


CS = construct_scores(B)

summary = pd.DataFrame({
    "respondent_type": "Member",
    "sus_items_answered": answered,
    "sus_score": sus.round(2),
    "sus_prorated": (answered < SUS_N) & sus.notna(),
    "sus_adjective": sus.map(lambda s: bangor_adjective(s) if pd.notna(s) else ""),
    "sus_grade": sus.map(lambda s: sl_grade(s) if pd.notna(s) else ""),
    "part2b_items_answered": B.notna().sum(axis=1),
    "PU_mean": CS["PU"].round(2),
    "PEOU_mean": CS["PEOU"].round(2),
    "BI_mean": CS["BI"].round(2),
    "overall_2B_mean": CS["Overall"].round(2),
})
admin_cs = {k: np.mean([admin["1B"][i - 1] for i in items]) for k, (_, items, _) in CONSTRUCTS.items()}
admin_cs["Overall"] = np.mean(admin["1B"])
summary.loc["R01"] = ["Administrator", 10, admin_sus, False, bangor_adjective(admin_sus), sl_grade(admin_sus),
                      13, round(admin_cs["PU"], 2), round(admin_cs["PEOU"], 2), round(admin_cs["BI"], 2),
                      round(admin_cs["Overall"], 2)]
summary = summary.sort_index()
summary.index.name = "code"
summary.to_csv(HERE / "study6_respondent_summary.csv")

# ---------------------------------------------------------------- demographics (codes only)
CHILI = "Chili pepper (sili, labuyo, espada)"
CROPS = {
    "R02": ["Bitter gourd (ampalaya)", "Okra", "Squash", "Tomato"],
    "R03": ["Melon (muskmelon)", "Watermelon"],
    "R04": ["Cucumber", "String beans", "Okra", "Eggplant"],
    "R05": ["String beans", "Cucumber", "Sweet corn", "Calamansi"],
    "R06": ["Bell pepper (atsal)"],
    "R07": ["Cucumber", "Bottle gourd (upo)", CHILI, "Squash"],
    "R08": ["Eggplant", "Cucumber", "Bottle gourd (upo)", "Watermelon"],
    "R09": ["Eggplant", "Bottle gourd (upo)", "Bell pepper (atsal)", CHILI, "Cucumber", "Pakudo (local name)",
            "Spring onion"],
    "R10": ["Eggplant", "Bitter gourd (ampalaya)", "Squash", "Bell pepper (atsal)"],
    "R11": ["Pinakbet vegetables (mixed)", "Cauliflower", "Lettuce", "Cabbage"],
    "R12": ["Eggplant"],
    "R13": ["Bell pepper (atsal)", "Pakudo (local name)", CHILI, "Okra"],
    "R14": [],
    "R15": ["Bitter gourd (ampalaya)", "Watermelon", "Squash", "Okra", "Cucumber"],
    "R16": ["String beans", "Bell pepper (atsal)", "Melon (muskmelon)", CHILI, "Squash"],
    "R17": ["Bitter gourd (ampalaya)", "Eggplant", "Bell pepper (atsal)", "Tomato", "Sweet corn", "Spring onion",
            "Sweet potato"],
    "R18": ["String beans", "Bitter gourd (ampalaya)", "Cucumber", "Tomato", "Eggplant"],
    "R19": ["Eggplant"],
    "R20": ["Pechay", "Sweet corn", "Eggplant"],
    "R21": ["Bitter gourd (ampalaya)", "Eggplant", "Squash", "Cucumber"],
    "R22": ["Bottle gourd (upo)", "Bitter gourd (ampalaya)", "Pechay", "Eggplant", "Tomato", "Okra", CHILI,
            "Bell pepper (atsal)"],
    "R23": ["Bottle gourd (upo)", "String beans", "Bitter gourd (ampalaya)", "Eggplant", "Watermelon"],
    "R24": ["Eggplant", "Okra", "Cucumber", "Bottle gourd (upo)", "String beans", CHILI,
            "Malabar spinach (alugbati)"],
    "R25": ["Bottle gourd (upo)", "Sponge gourd (sikwa)"],
    "R26": ["Eggplant", "String beans", "Cucumber", "Bottle gourd (upo)"],
    "R27": ["Cauliflower", "Bitter gourd (ampalaya)", "String beans", "Pechay", "Bell pepper (atsal)"],
    "R28": ["Bitter gourd (ampalaya)", "Tomato"],
}
# Problems: P = insects/pests, D = plant disease, O = others (specification or "unspecified")
PROBLEMS = {
    "R02": "P", "R03": "PD", "R04": "PDO:unspecified", "R05": "PD", "R06": "PD", "R07": "PO:unspecified",
    "R08": "PD", "R09": "PO:unspecified", "R10": "PD", "R11": "PO:Typhoon", "R12": "PDO:unspecified",
    "R13": "P", "R14": "", "R15": "PD", "R16": "PD", "R17": "PDO:White flies", "R18": "PO:unspecified",
    "R19": "PD", "R20": "PD", "R21": "PD", "R22": "PD", "R23": "P",
    "R24": "PDO:Theft by neighbors", "R25": "PD", "R26": "PD", "R27": "PDO:unspecified", "R28": "PD",
}

# Role, sex, coded years and coded income are read from Section 5 of the transcription.
demo_rows = []
for l in section(r"## 5\. ", r"## 6\. "):
    m = re.match(r"\| (R\d\d) \|(.*)\|\s*$", l)
    if not m:
        continue
    f = [x.strip() for x in m.group(2).split("|")]
    code = m.group(1)
    role_raw, sex_raw, years_coded, income_coded = f[0], f[1], f[3], f[7]
    role = ("Officer" if role_raw.startswith("Officer") else
            "Member" if role_raw.startswith("Member") else "Others (applicant for membership)")
    sex = "Female" if sex_raw.startswith("Female") else "Male"
    years = float(years_coded)
    income = None if income_coded == "missing" else float(income_coded.replace(",", ""))
    p = PROBLEMS[code]
    other = p.split("O:")[1] if "O:" in p else ""
    demo_rows.append(dict(code=code, role=role, sex=sex, years_member=years, crops="; ".join(CROPS[code]),
                          n_crops=len(CROPS[code]), insects_pests="P" in p.split("O:")[0],
                          plant_disease="D" in p.split("O:")[0], others=bool(other), others_specified=other,
                          annual_income_php=income))
demo = pd.DataFrame(demo_rows).set_index("code")
assert len(demo) == 27


def years_group(y: float) -> str:
    if y < 1:
        return "Less than 1 year"
    if y < 2:
        return "1 to less than 2 years"
    if y < 3:
        return "2 to less than 3 years"
    return "3 years or more"


def income_group(v) -> str:
    if v is None or pd.isna(v):
        return "Not reported"
    if v <= 50_000:
        return "₱50,000 or less"
    if v <= 100_000:
        return "₱50,001 – ₱100,000"
    if v <= 150_000:
        return "₱100,001 – ₱150,000"
    return "Above ₱150,000"


demo["years_group"] = demo["years_member"].map(years_group)
demo["income_group"] = demo["annual_income_php"].map(income_group)
demo.to_csv(HERE / "study6_demographics.csv")

# ---------------------------------------------------------------- tables (markdown)
out: list[str] = []
w = out.append
N_MEM = 27


def pct(n: int, d: int) -> str:
    return f"{100 * n / d:.2f}"


def freq_table(series: pd.Series, order: list[str], title: str, denom: int) -> None:
    w(f"| {title} | f | % |")
    w("|---|---:|---:|")
    for k in order:
        n = int((series == k).sum())
        w(f"| {k} | {n} | {pct(n, denom)} |")
    w(f"| **Total** | **{int(series.isin(order).sum())}** | **{pct(int(series.isin(order).sum()), denom)}** |")
    w("")


w("# Study 6 analysis tables (generated by study6_analysis.py; do not edit by hand)\n")
w(f"Cross-check of summary tables (Sections 3-4) against per-form tables (Section 8): "
  f"{'all match' if not mismatch else 'MISMATCHES: ' + repr(mismatch)}\n")

# Demographics
w("## D1. Role\n")
freq_table(demo["role"], ["Member", "Officer", "Others (applicant for membership)"], "Role in Baybayani", N_MEM)
w("## D2. Sex\n")
freq_table(demo["sex"], ["Male", "Female"], "Sex", N_MEM)
w("## D3. Years as member\n")
freq_table(demo["years_group"], ["Less than 1 year", "1 to less than 2 years", "2 to less than 3 years",
                                 "3 years or more"], "Years as member", N_MEM)
d = describe(demo["years_member"])
w(f"Years as member (coded): n = {d['n']}, mean = {f2(d['mean'])}, SD = {f2(d['sd'])}, "
  f"median = {d['median']:g}, range = {d['min']:g}–{d['max']:g}\n")

w("## D4. Crops produced (multiple response)\n")
crop_resp = demo[demo["n_crops"] > 0]
n_crop_resp = len(crop_resp)
counts: dict[str, int] = {}
for cl in CROPS.values():
    for c in set(cl):
        counts[c] = counts.get(c, 0) + 1
w(f"Respondents who answered: {n_crop_resp} of {N_MEM} (R14 left Q4 blank). "
  f"Crops per respondent: mean = {f2(crop_resp['n_crops'].mean())}, median = {crop_resp['n_crops'].median():g}, "
  f"range = {crop_resp['n_crops'].min()}–{crop_resp['n_crops'].max()}.\n")
w(f"| Crop | f | % of {n_crop_resp} respondents |")
w("|---|---:|---:|")
for c, n in sorted(counts.items(), key=lambda kv: (-kv[1], kv[0])):
    w(f"| {c} | {n} | {pct(n, n_crop_resp)} |")
w("")

w("## D5. Problems encountered when planting (multiple response)\n")
prob_resp = demo[demo["insects_pests"] | demo["plant_disease"] | demo["others"]]
npr = len(prob_resp)
w(f"Respondents who answered: {npr} of {N_MEM} (R14 left Q5 blank).\n")
w(f"| Problem | f | % of {npr} respondents |")
w("|---|---:|---:|")
for lab, col in [("Insects/pests", "insects_pests"), ("Plant disease", "plant_disease"), ("Others", "others")]:
    n = int(demo[col].sum())
    w(f"| {lab} | {n} | {pct(n, npr)} |")
for spec in ["Typhoon", "White flies", "Theft by neighbors", "unspecified"]:
    n = int((demo["others_specified"] == spec).sum())
    lab = "Others, not specified" if spec == "unspecified" else spec
    w(f"| &nbsp;&nbsp;&nbsp;{lab} | {n} | {pct(n, npr)} |")
w("")
combo = demo.apply(lambda r: " + ".join([x for x, c in [("Insects/pests", r.insects_pests),
                                                         ("Plant disease", r.plant_disease),
                                                         ("Others", r.others)] if c]) or "No answer", axis=1)
w("| Combination | f | % of 27 |")
w("|---|---:|---:|")
for k, n in combo.value_counts().items():
    w(f"| {k} | {n} | {pct(n, N_MEM)} |")
w("")

w("## D6. Estimated annual farm income\n")
freq_table(demo["income_group"], ["₱50,000 or less", "₱50,001 – ₱100,000", "₱100,001 – ₱150,000",
                                  "Above ₱150,000", "Not reported"], "Annual farm income", N_MEM)
d = describe(demo["annual_income_php"])
w(f"Reported income (n = {d['n']}): mean = ₱{d['mean']:,.2f}, SD = ₱{d['sd']:,.2f}, median = ₱{d['median']:,.0f}, "
  f"range = ₱{d['min']:,.0f}–₱{d['max']:,.0f}\n")

# SUS
w("## S1. SUS score per member\n")
w("| Code | Items answered | SUS | Note | Bangor adjective | Acceptability | Sauro–Lewis grade |")
w("|---|---:|---:|---|---|---|---|")
for code in A.index:
    s = sus[code]
    if pd.isna(s):
        w(f"| {code} | {answered[code]} | – | not scored (no Part 2A answers) | – | – | – |")
    else:
        note = f"prorated ({SUS_N - answered[code]} missing)" if answered[code] < SUS_N else ""
        w(f"| {code} | {answered[code]} | {f2(s)} | {note} | {bangor_adjective(s)} | {bangor_acceptability(s)} | "
          f"{sl_grade(s)} |")
w("")

w("## S2. SUS summary (members)\n")
w("| Basis | n | Mean | SD | Median | Min | Max | 95% CI of mean |")
w("|---|---:|---:|---:|---:|---:|---:|---|")
for lab, ser in [("All scored (≤2 missing, prorated) — reported", sus),
                 ("Complete cases only (check)", sus_complete)]:
    d = describe(ser)
    se = d["sd"] / math.sqrt(d["n"])
    t = stats.t.ppf(0.975, d["n"] - 1)
    w(f"| {lab} | {d['n']} | {f2(d['mean'])} | {f2(d['sd'])} | {f2(d['median'])} | {f2(d['min'])} | "
      f"{f2(d['max'])} | {f2(d['mean'] - t * se)}–{f2(d['mean'] + t * se)} |")
w("")
m_sus = sus.mean()
w(f"Mean SUS {f2(m_sus)}: Bangor adjective = {bangor_adjective(m_sus)}; acceptability = "
  f"{bangor_acceptability(m_sus)}; Sauro–Lewis grade = {sl_grade(m_sus)}.\n")

w("## S3. Distribution of member SUS scores\n")
w("| Sauro–Lewis grade | SUS range | f | % of scored |")
w("|---|---|---:|---:|")
scored = sus.dropna()
uppers = [100.0] + [lo - 0.1 for lo, _, _ in SAURO_LEWIS[:-1]]
for (lo, g, _), hi in zip(SAURO_LEWIS, uppers):
    n = int(scored.map(sl_grade).eq(g).sum())
    if n:
        w(f"| {g} | {lo:.1f}–{hi:.1f} | {n} | {pct(n, len(scored))} |")
w("")
w("| Bangor adjective (nearest mean) | f | % of scored |")
w("|---|---:|---:|")
for a, _ in BANGOR_ADJ[::-1]:
    n = int(scored.map(bangor_adjective).eq(a).sum())
    if n:
        w(f"| {a} | {n} | {pct(n, len(scored))} |")
w("")
w("| Acceptability (Bangor et al., 2008) | f | % of scored |")
w("|---|---:|---:|")
for a in ["Acceptable", "Marginal (high)", "Marginal (low)", "Not acceptable"]:
    n = int(scored.map(bangor_acceptability).eq(a).sum())
    w(f"| {a} | {n} | {pct(n, len(scored))} |")
w("")

w("## S4. SUS items (members): raw responses and score contributions\n")
w("| Item | Statement | Tone | n | Raw mean (1–5) | SD | % agree (4–5) | Mean contribution (0–4) |")
w("|---|---|---|---:|---:|---:|---:|---:|")
for i in range(1, 11):
    col = A[f"Q{i}"].dropna()
    agree = (col >= 4).sum()
    tone = "positive" if i % 2 else "negative"
    w(f"| Q{i} | {SUS_ITEMS[i - 1]} | {tone} | {len(col)} | {f2(col.mean())} | {f2(col.std(ddof=1))} | "
      f"{pct(agree, len(col))} | {f2(C[f'Q{i}'].mean())} |")
w("")
pos_items = A[[f"Q{i}" for i in (1, 3, 5, 7, 9)]]
neg_items = A[[f"Q{i}" for i in (2, 4, 6, 8, 10)]]
w(f"Mean raw agreement, positive items = {f2(pos_items.stack().mean())}; negative items = "
  f"{f2(neg_items.stack().mean())} (on 1–5).\n")
alpha_sus, n_a = cronbach_alpha(C)
alpha_pos, n_p = cronbach_alpha(C[[f"Q{i}" for i in (1, 3, 5, 7, 9)]])
alpha_neg, n_n = cronbach_alpha(C[[f"Q{i}" for i in (2, 4, 6, 8, 10)]])
w(f"Cronbach's alpha, SUS 10 items (scored contributions, complete cases n = {n_a}) = {f2(alpha_sus)}; "
  f"positive items only = {f2(alpha_pos)}; negative items only = {f2(alpha_neg)}.\n")
inter = C[[f"Q{i}" for i in range(1, 11)]].corr()
pos_neg = [inter.loc[f"Q{i}", f"Q{j}"] for i in (1, 3, 5, 7, 9) for j in (2, 4, 6, 8, 10)]
w(f"Mean correlation between positive-item and negative-item contributions = {f2(np.mean(pos_neg))}.\n")
both = pd.concat([sus, CS["PEOU"], CS["Overall"]], axis=1, keys=["SUS", "PEOU", "Overall"]).dropna()
rho1, p1 = stats.spearmanr(both["SUS"], both["PEOU"])
rho2, p2 = stats.spearmanr(both["SUS"], both["Overall"])
w(f"Spearman correlation of SUS with Part 2B ease of use: rho = {f2(rho1)}, p = {p1:.3f}; with Part 2B overall: "
  f"rho = {f2(rho2)}, p = {p2:.3f} (n = {len(both)}).\n")

# Part 2B
w("## B1. Part 2B items (members)\n")
w("| Construct | Item | Statement | n | Mean | SD | Verbal interpretation |")
w("|---|---|---|---:|---:|---:|---|")
for i in range(1, 14):
    col = B[f"Q{i}"].dropna()
    w(f"| {construct_of(i)} | Q{i} | {B_ITEMS[i - 1]} | {len(col)} | {f2(col.mean())} | {f2(col.std(ddof=1))} | "
      f"{seven_label(col.mean())} |")
w("")

w("## B2. Part 2B constructs (members)\n")
w("| Construct | Items | Respondents scored (n) | Mean | SD | Median | Range | Cronbach's α (complete n) | "
  "Verbal interpretation |")
w("|---|---|---:|---:|---:|---:|---|---|---|")
for k, (name, items, need) in list(CONSTRUCTS.items()) + [("Overall", ("All Part 2B items", list(range(1, 14)),
                                                                       OVERALL_MIN))]:
    d = describe(CS[k])
    a, na = cronbach_alpha(B[[f"Q{i}" for i in items]])
    w(f"| {name} | Q{items[0]}–Q{items[-1]} | {d['n']} | {f2(d['mean'])} | {f2(d['sd'])} | {f2(d['median'])} | "
      f"{f2(d['min'])}–{f2(d['max'])} | {f2(a)} ({na}) | {seven_label(d['mean'])} |")
w("")
excluded = {k: list(CS.index[CS[k].isna()]) for k in CS.columns}
w("Respondents without a construct score (fewer than half the items answered): " +
  "; ".join(f"{k}: {', '.join(v) if v else 'none'}" for k, v in excluded.items()) + "\n")

w("## B3. Distribution of member construct scores by verbal interpretation\n")
labels = [lab for _, lab in SEVEN_POINT]
w("| Interpretation | " + " | ".join(f"{k} f (%)" for k in ["PU", "PEOU", "BI", "Overall"]) + " |")
w("|---|" + "---:|" * 4)
for lab in labels:
    cells = []
    for k in ["PU", "PEOU", "BI", "Overall"]:
        s = CS[k].dropna()
        n = int(s.map(seven_label).eq(lab).sum())
        cells.append(f"{n} ({pct(n, len(s))})")
    w(f"| {lab} | " + " | ".join(cells) + " |")
w("")

# Admin
w("## A1. Administrator (R01)\n")
w("| Item | SUS statement | Response (1–5) | Contribution (0–4) |")
w("|---|---|---:|---:|")
for i, (x, c) in enumerate(zip(admin["1A"], admin_c), 1):
    w(f"| Q{i} | {SUS_ITEMS[i - 1]} | {x} | {c} |")
w(f"| | **SUS score** | | **{admin_sus:.1f}** |")
w("")
w(f"Admin SUS {admin_sus:.1f}: Bangor adjective = {bangor_adjective(admin_sus)}; acceptability = "
  f"{bangor_acceptability(admin_sus)}; Sauro–Lewis grade = {sl_grade(admin_sus)}.\n")
w("| Construct | Item | Statement | Response (1–7) | Verbal interpretation |")
w("|---|---|---|---:|---|")
for i, x in enumerate(admin["1B"], 1):
    w(f"| {construct_of(i)} | Q{i} | {ADMIN_B_ITEMS[i - 1]} | {x} | {seven_label(x)} |")
w("")
w("| Construct | Mean of items | Verbal interpretation |")
w("|---|---:|---|")
for k in ["PU", "PEOU", "BI", "Overall"]:
    name = CONSTRUCTS[k][0] if k in CONSTRUCTS else "All Part 1B items"
    w(f"| {name} | {f2(admin_cs[k])} | {seven_label(admin_cs[k])} |")
w("")

(HERE / "study6_tables.md").write_text("\n".join(out), encoding="utf-8")
print("\n".join(out))
if mismatch:
    raise SystemExit(f"Cross-check failed: {mismatch}")
