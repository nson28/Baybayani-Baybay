"""Figures for the Study 6 LaTeX report.

Reads the CSVs written by ../analysis/study6_analysis.py and saves vector PDFs in ./figures/.
Run:  python evaluation/report/make_figures.py
"""
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import pandas as pd

HERE = Path(__file__).resolve().parent
DATA = HERE.parent / "analysis"
OUT = HERE / "figures"
OUT.mkdir(exist_ok=True)

# Palette (validated against a white surface): blue = members / agree, orange = administrator,
# red = disagree, gray = neutral; ink and hairlines from the reference chart chrome.
BLUE, ORANGE, RED = "#2a78d6", "#eb6834", "#e34948"
NEUTRAL = "#c3c2b7"
INK, INK2, MUTED, GRID = "#0b0b0b", "#52514e", "#898781", "#e1e0d9"
BAND = "#f3f2ee"

plt.rcParams.update({
    "font.family": "sans-serif",
    "font.sans-serif": ["Arial", "DejaVu Sans"],
    "font.size": 9,
    "axes.edgecolor": NEUTRAL,
    "axes.labelcolor": INK2,
    "xtick.color": INK2,
    "ytick.color": INK,
    "axes.spines.top": False,
    "axes.spines.right": False,
    "pdf.fonttype": 42,
})

scores = pd.read_csv(DATA / "study6_scores.csv")
summary = pd.read_csv(DATA / "study6_respondent_summary.csv", index_col="code")
demo = pd.read_csv(DATA / "study6_demographics.csv", index_col="code")
members = scores[scores.respondent_type == "Member"]


def save(fig, name):
    fig.savefig(OUT / f"{name}.pdf", bbox_inches="tight")
    plt.close(fig)


# ---------------------------------------------------------------- Figure: crops
crops = demo["crops"].dropna().str.split("; ")
n_resp = len(crops)
counts = crops.explode().value_counts()
counts = counts[counts >= 2]
counts = counts.loc[sorted(counts.index, key=lambda c: (-counts[c], c))][::-1]
fig, ax = plt.subplots(figsize=(6.0, 4.0))
pct = counts / n_resp * 100
ax.barh(counts.index, pct, color=BLUE, height=0.7, edgecolor="white", linewidth=1)
for y, (p, f) in enumerate(zip(pct, counts)):
    ax.text(p + 0.8, y, f"{f} ({p:.1f}%)", va="center", fontsize=8, color=INK2)
ax.set_xlim(0, 65)
ax.set_xlabel(f"Percentage of members who answered (n = {n_resp})")
ax.xaxis.grid(True, color=GRID, linewidth=0.6)
ax.set_axisbelow(True)
ax.tick_params(axis="y", length=0)
save(fig, "fig_crops")

# ---------------------------------------------------------------- Figure: SUS distribution
sus = summary.loc[summary.respondent_type == "Member", "sus_score"].dropna().sort_values()
admin_sus = float(summary.loc["R01", "sus_score"])
grades = [(0, 51.7, "F"), (51.7, 62.7, "D"), (62.7, 65.0, "C−"), (65.0, 71.1, "C"), (71.1, 72.6, "C+"),
          (72.6, 74.1, "B−"), (74.1, 77.2, "B"), (77.2, 78.9, "B+"), (78.9, 80.8, "A−"),
          (80.8, 84.1, "A"), (84.1, 100, "A+")]
fig, ax = plt.subplots(figsize=(6.3, 2.6))
for i, (lo, hi, g) in enumerate(grades):
    if i % 2 == 0:
        ax.axvspan(lo, hi, color=BAND, zorder=0, linewidth=0)
    vlo, vhi = max(lo, 30), min(hi, 90)
    if vhi - vlo >= 2.0:
        ax.text((vlo + vhi) / 2, 10.25, g, ha="center", va="center", fontsize=7, color=MUTED)
# stacked dots: one dot per member, stacked by identical score
stack = {}
for s in sus:
    key = round(s, 2)
    stack[key] = stack.get(key, 0) + 1
    ax.scatter(s, stack[key], s=34, color=BLUE, edgecolor="white", linewidth=0.8, zorder=3)
ax.scatter(admin_sus, 1, s=46, marker="D", color=ORANGE, edgecolor="white", linewidth=0.8, zorder=3)
ax.annotate(f"Administrator\n{admin_sus:.1f}", (admin_sus, 1), xytext=(admin_sus, 3.6), ha="center",
            fontsize=7.5, color=INK2, arrowprops=dict(arrowstyle="-", color=MUTED, lw=0.6))
m = sus.mean()
ax.axvline(m, color=INK, lw=1.0, zorder=2)
ax.text(m - 1.0, 8.6, f"Member mean {m:.2f}", ha="right", fontsize=7.5, color=INK)
ax.axvline(68, color=MUTED, lw=0.9, ls=(0, (3, 2)), zorder=2)
ax.text(69.0, 8.6, "Benchmark\naverage 68", ha="left", fontsize=7.5, color=INK2, va="center")
ax.set_xlim(30, 90)
ax.set_ylim(0.2, 10.8)
ax.set_yticks([])
ax.spines["left"].set_visible(False)
ax.set_xlabel("SUS score (0–100); shaded bands = Sauro–Lewis grades")
save(fig, "fig_sus_distribution")

# ---------------------------------------------------------------- Figure: SUS item agreement
sus_labels = {
    1: "Would like to use it frequently", 3: "Easy to use", 5: "Functions well integrated",
    7: "Most people would learn it quickly", 9: "Felt very confident using it",
    2: "Unnecessarily complex", 4: "Need support of a technical person", 6: "Too much inconsistency",
    8: "Very awkward to use", 10: "Needed to learn a lot first",
}
order = [1, 3, 5, 7, 9, 2, 4, 6, 8, 10]
a = members[members.part == "2A"].dropna(subset=["response"])
rows = []
for q in order:
    r = a[a["item"] == q]["response"]
    n = len(r)
    rows.append((q, (r <= 2).sum() / n * 100, (r == 3).sum() / n * 100, (r >= 4).sum() / n * 100, n))
fig, ax = plt.subplots(figsize=(6.3, 3.6))
ypos = []
y = 0.9
heads = []
for i, (q, dis, neu, agr, n) in enumerate(rows):
    if i == 5:
        y += 1.4  # gap and header row between positive and negative groups
    ypos.append(y)
    left = 0
    for val, col in [(dis, RED), (neu, NEUTRAL), (agr, BLUE)]:
        ax.barh(y, val, left=left, color=col, height=0.72, edgecolor="white", linewidth=1.2)
        if val >= 7:
            ax.text(left + val / 2, y, f"{val:.0f}%", ha="center", va="center", fontsize=7,
                    color="#ffffff" if col != NEUTRAL else INK)
        left += val
    y += 1
ax.set_yticks(ypos)
ax.set_yticklabels([f"Q{q}  {sus_labels[q]}" for q, *_ in rows])
ax.set_xlim(0, 100)
ax.set_xlabel("Percentage of members (n = 24–26 per item)")
ax.tick_params(axis="y", length=0)
ax.text(0, ypos[0] - 0.85, "Positively worded items (agreeing = better usability)", ha="left", va="center",
        fontsize=8, color=INK, fontweight="bold")
ax.text(0, ypos[5] - 0.85, "Negatively worded items (agreeing = worse usability)", ha="left", va="center",
        fontsize=8, color=INK, fontweight="bold")
ax.set_ylim(ypos[-1] + 0.6, -0.4)
handles = [plt.Rectangle((0, 0), 1, 1, color=c) for c in (RED, NEUTRAL, BLUE)]
ax.legend(handles, ["Disagree (1–2)", "Neutral (3)", "Agree (4–5)"], ncol=3, frameon=False,
          loc="lower center", bbox_to_anchor=(0.5, 1.06), fontsize=8)
save(fig, "fig_sus_items")

# ---------------------------------------------------------------- Figure: Part 2B item means
b_labels = {
    1: "Place orders more quickly", 2: "More convenient to order", 3: "Helps keep track of orders",
    4: "Improves online shopping", 5: "Useful for buying products",
    6: "Learning it was easy", 7: "Easy to find products", 8: "Checkout easy to follow",
    9: "Interface easy to understand", 10: "Easy to become skillful",
    11: "Will use it for future orders", 12: "Prefer app over buying in person", 13: "Would recommend it",
}
groups = [("Perceived usefulness", range(1, 6)), ("Perceived ease of use", range(6, 11)),
          ("Intention to use", range(11, 14))]
b = members[members.part == "2B"].dropna(subset=["response"])
bands = [(3.57, 4.43, "Neutral"), (4.43, 5.29, "Slightly\nagree"), (5.29, 6.15, "Agree"),
         (6.15, 7.0, "Extremely\nagree")]
fig, ax = plt.subplots(figsize=(6.3, 4.4))
for i, (lo, hi, lab) in enumerate(bands):
    if i % 2 == 0:
        ax.axvspan(lo, hi, color=BAND, zorder=0, linewidth=0)
    ax.text((lo + hi) / 2, -1.25, lab, ha="center", va="center", fontsize=7.5, color=MUTED)
y = 0
ticks, labels = [], []
for gname, items in groups:
    cmean = summary.loc[summary.respondent_type == "Member",
                        {"Perceived usefulness": "PU_mean", "Perceived ease of use": "PEOU_mean",
                         "Intention to use": "BI_mean"}[gname]].mean()
    ax.text(3.6, y, f"{gname}: construct mean {cmean:.2f}", fontsize=8, fontweight="bold", color=INK,
            va="center")
    y += 1
    for q in items:
        r = b[b["item"] == q]["response"]
        mu = r.mean()
        ax.scatter(mu, y, s=38, color=BLUE, edgecolor="white", linewidth=0.8, zorder=3)
        ax.text(mu + 0.06, y, f"{mu:.2f}", va="center", fontsize=7.5, color=INK2)
        ticks.append(y)
        labels.append(f"Q{q}  {b_labels[q]}")
        y += 1
    y += 0.4
ax.set_yticks(ticks)
ax.set_yticklabels(labels)
ax.invert_yaxis()
ax.set_xlim(3.57, 7.0)
ax.set_ylim(y - 0.4, -1.8)
ax.set_xticks([4, 4.5, 5, 5.5, 6, 6.5, 7])
ax.set_xlabel("Item mean (1 = extremely disagree, 7 = extremely agree)")
ax.tick_params(axis="y", length=0)
ax.xaxis.grid(True, color=GRID, linewidth=0.6)
ax.set_axisbelow(True)
save(fig, "fig_part2b_items")

print("figures written to", OUT)
