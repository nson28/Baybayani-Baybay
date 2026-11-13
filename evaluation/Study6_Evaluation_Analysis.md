# Study 6: Analysis of the Evaluation of the Baybayani MIS and Mobile Application

| | |
|---|---|
| Project | *Farm to Table: A Management Information System for Farmers and Food Business Establishments in Baybay City, Leyte* (DCST.0824-0825) |
| Study | Study 6: Evaluation of the developed management information system and mobile application (*Baybayani* e-commerce platform) |
| Component Leader | Jomari Joseph A. Barrera, DCST, Visayas State University |
| Date of evaluation | November 12, 2026 |
| Respondents | 28 (1 administrator, 27 members/farmers) |
| Data source | [*Study6_Evaluation_Transcription.md*](Study6_Evaluation_Transcription.md), verified against the paper forms on November 13, 2026 |
| Analysis files | [`analysis/`](analysis/): `study6_analysis.py` (script), `study6_scores.csv` (tidy item responses), `study6_respondent_summary.csv`, `study6_demographics.csv`, `study6_tables.md` (all generated tables) |
| Prepared | November 13, 2026 |

Respondents are identified by code only (R01–R28). No names appear in this report or in the analysis files.

---

## 1. Methods

### 1.1 Respondents
The evaluation was carried out on November 12, 2026, with **28 respondents**: the platform **administrator (R01)** and **27 members/farmers of Baybayani (R02–R28)**. All 28 forms were kept in the sample. Two of the member forms were answered by officers (R11, R15) and one by an applicant for membership (R04). They were analyzed with the member group because they answered the member form, and their roles are reported as they answered them.

### 1.2 Instruments
Two forms were used. Both have the same two parts.

| Part | Administrator form (R01) | Member form (R02–R28) | Scale |
|---|---|---|---|
| Perceived usability | Part 1A: the 10-item System Usability Scale (SUS; Brooke, 1996) | Part 2A: the same 10 SUS items (English with Cebuano) | 1 = strongly disagree … 5 = strongly agree |
| Usefulness, ease of use and intention | Part 1B: 13 items on administrator tasks (recording, managing and reporting orders) | Part 2B: 13 items on ordering through the app | 1 = extremely disagree … 4 = neutral … 7 = extremely agree |
| Profile | – | Part 1: role, sex, years as member, crops produced, problems in planting, estimated annual farm income | – |
| Open-ended | Comments/suggestions | Comments/suggestions | – |

The 13 items in Parts 1B and 2B follow the constructs of the Technology Acceptance Model (Davis, 1989): **perceived usefulness (PU)**, items 1–5; **perceived ease of use (PEOU)**, items 6–10; and **intention to use or recommend (BI)**, items 11–13.

### 1.3 Scoring and interpretation
**SUS.** Standard scoring was used. Each odd (positively worded) item contributes *response − 1*, each even (negatively worded) item contributes *5 − response*, and the sum of the 10 contributions is multiplied by 2.5 to give a score of 0–100. Scores were interpreted in three ways:
- the **adjective rating** of Bangor, Kortum and Miller (2009): the score is given the adjective whose mean SUS is closest (Poor 35.7, OK 50.9, Good 71.4, Excellent 85.5, Best imaginable 90.9);
- the **acceptability range** of Bangor, Kortum and Miller (2008): Not acceptable below 50, Marginal 50–70 (low 50–62, high 63–70), Acceptable above 70;
- the **letter grade** on the Sauro–Lewis curved grading scale (Sauro & Lewis, 2016), which ranks a score against a large benchmark of SUS studies. On this scale 68 is about average (C), 51.7–62.6 is D, and below 51.7 is F.

**Parts 1B and 2B (1–7).** Item means, construct means and standard deviations were computed. Means were interpreted with **equal-interval cut-offs** (width = (7 − 1) / 7 ≈ 0.86), labelled with the form's own response anchors:

| Mean | Verbal interpretation |
|---|---|
| 6.15 – 7.00 | Extremely agree |
| 5.29 – 6.14 | Agree |
| 4.43 – 5.28 | Slightly agree |
| 3.57 – 4.42 | Neutral |
| 2.72 – 3.56 | Slightly disagree |
| 1.86 – 2.71 | Disagree |
| 1.00 – 1.85 | Extremely disagree |

**Reliability.** Internal consistency was estimated with Cronbach's alpha and interpreted using George and Mallery (2003): ≥ .90 excellent, ≥ .80 good, ≥ .70 acceptable, ≥ .60 questionable, below .60 poor.

**Profile and comments.** The profile is reported as frequencies and percentages. Crops and problems are multiple-response items, so their percentages are based on the number of respondents who answered and can add up to more than 100%. Comments were grouped by theme.

### 1.4 Handling of missing data
Unanswered items (`BLANK` on the form, confirmed on paper) were treated as missing. No values were imputed except in the SUS proration described below.

| Data | Rule applied | Effect |
|---|---|---|
| SUS (Part 2A) | A respondent who skipped **one or two** items is **prorated**: the mean of the answered item contributions × 10 × 2.5. A respondent who skipped more is not scored. | 21 complete cases plus 5 prorated (R07 skipped 2 items; R19, R21, R24 and R25 skipped 1 each) gives **n = 26**. R14 answered none of Part 2A and has no SUS score. Using complete cases only gives nearly the same result (mean 54.05 vs 54.40; Table 6). |
| Part 2B constructs | A construct score is the mean of the answered items **if at least half the items were answered** (PU ≥ 3 of 5, PEOU ≥ 3 of 5, BI ≥ 2 of 3, all 13 items ≥ 7 of 13). Otherwise it is missing. | R08 answered 6 of 13 items, so it has no PU, BI or overall score. R23 answered 1 of the 3 BI items, so it has no BI score. |
| Item statistics | Each item uses all available answers, so item *n* varies (24–27). | – |
| Cronbach's alpha | Complete cases only for the items involved. | *n* is shown with each alpha. |
| Profile | Blank or illegible answers are reported as "not reported". Years as member and income were coded as recorded in Section 1.1 of the transcription. Monthly incomes were annualized (R07, R20) and stated ranges were coded at their midpoint (R24: 2–3 years = 2.5). | Income is not reported for 9 of the 27 members. |

### 1.5 Data processing
The verified scores were extracted from the transcription and checked automatically: the summary tables matched every per-form table, and all values fell within their scale range. All statistics were computed with a Python script (`analysis/study6_analysis.py`; pandas, SciPy). Selected SUS scores were also recomputed by hand to check the script. Values are rounded to two decimals.

---

## 2. Results

### 2.1 Profile of the member respondents

**Table 1. Role, sex and years as member (n = 27)**

| Characteristic | Category | f | % |
|---|---|---:|---:|
| Role in Baybayani | Member | 24 | 88.89 |
| | Officer | 2 | 7.41 |
| | Others (applicant for membership) | 1 | 3.70 |
| Sex | Male | 19 | 70.37 |
| | Female | 8 | 29.63 |
| Years as member | Less than 1 year | 2 | 7.41 |
| | 1 to less than 2 years | 3 | 11.11 |
| | 2 to less than 3 years | 17 | 62.96 |
| | 3 years or more | 5 | 18.52 |

Years as member: mean = 2.01, SD = 0.72, median = 2, range = 0–3.

Most respondents were rank-and-file **members (88.89%)** and **male (70.37%)**. Most had been with Baybayani for **two to less than three years (62.96%)**, so most of the evaluators joined around 2024. One respondent was still applying for membership.

**Table 2. Crops produced for Baybayani (multiple response; n = 26 who answered)**

| Crop | f | % |
|---|---:|---:|
| Eggplant (talong) | 14 | 53.85 |
| Bitter gourd (ampalaya/paliya) | 10 | 38.46 |
| Cucumber (pipino) | 10 | 38.46 |
| Bell pepper (atsal) | 8 | 30.77 |
| Bottle gourd (upo) | 8 | 30.77 |
| String beans (batong) | 8 | 30.77 |
| Chili pepper (sili, labuyo, espada) | 6 | 23.08 |
| Okra | 6 | 23.08 |
| Squash (kalabasa) | 6 | 23.08 |
| Tomato (kamatis) | 5 | 19.23 |
| Watermelon (pakwan) | 4 | 15.38 |
| Pechay | 3 | 11.54 |
| Sweet corn | 3 | 11.54 |
| Cauliflower | 2 | 7.69 |
| Melon (muskmelon) | 2 | 7.69 |
| Pakudo (local name)ᵃ | 2 | 7.69 |
| Spring onion (sibuyas dahon) | 2 | 7.69 |
| Cabbage; calamansi; lettuce; Malabar spinach (alugbati); pinakbet vegetables (mixed); sponge gourd (sikwa); sweet potato (kamote) | 1 each | 3.85 each |

ᵃ Written as "pakodo" (R09) and "pakudo" (R13); the crop could not be identified and is reported by its local name. R14 left this item blank.

Members grew **4.08 crops on average** (median 4, range 1–8). Production centers on common lowland vegetables. **Eggplant** was the most common (53.85%), followed by **bitter gourd and cucumber** (38.46% each), then **bell pepper, bottle gourd and string beans** (30.77% each). These are the products most likely to be listed on the platform.

**Table 3. Problems encountered when planting (multiple response; n = 26 who answered)**

| Problem | f | % |
|---|---:|---:|
| Insects/pests | 26 | 100.00 |
| Plant disease | 19 | 73.08 |
| Others | 9 | 34.62 |
| — typhoon | 1 | 3.85 |
| — white flies | 1 | 3.85 |
| — theft by neighbors | 1 | 3.85 |
| — not specified | 6 | 23.08 |

**Every member who answered reported insect and pest problems**, and almost three in four (19 of 26) also reported plant disease. The other problems written in were weather (typhoon), a specific pest (white flies) and theft from the farm.

**Table 4. Estimated annual farm income (n = 27)**

| Annual farm income | f | % |
|---|---:|---:|
| ₱50,000 or less | 7 | 25.93 |
| ₱50,001 – ₱100,000 | 7 | 25.93 |
| ₱100,001 – ₱150,000 | 2 | 7.41 |
| Above ₱150,000 | 2 | 7.41 |
| Not reported | 9 | 33.33 |

Among the 18 who reported income: mean = ₱83,333.33, SD = ₱58,132.71, median = ₱82,500, range = ₱10,000–₱200,000.

A third of the members did not give an income. Among those who did, **most (14 of 18) earned ₱100,000 or less a year from farming**, and the median was ₱82,500. The amounts varied widely, from ₱10,000 to ₱200,000. Income was self-estimated, so these figures should be read as approximate.

### 2.2 Perceived usability of the platform (SUS, members)

**Table 5. SUS score of the members**

| Statistic | Value |
|---|---|
| n (scored) | 26 |
| Mean | **54.40** |
| SD | 7.93 |
| Median | 52.50 |
| Range | 35.00 – 77.50 |
| 95% confidence interval of the mean | 51.20 – 57.61 |
| Adjective rating (Bangor et al., 2009) | **OK** |
| Acceptability (Bangor et al., 2008) | **Marginal (low)** |
| Sauro–Lewis grade | **D** (15th–34th percentile) |

**Table 6. Check: prorated vs complete-case SUS**

| Basis | n | Mean | SD | Median | Range |
|---|---:|---:|---:|---:|---|
| Prorated (reported) | 26 | 54.40 | 7.93 | 52.50 | 35.00–77.50 |
| Complete cases only | 21 | 54.05 | 8.42 | 52.50 | 35.00–77.50 |

**Table 7. Distribution of member SUS scores (n = 26)**

| Sauro–Lewis grade | f | % | | Adjective rating | f | % | | Acceptability | f | % |
|---|---:|---:|---|---|---:|---:|---|---|---:|---:|
| B+ | 1 | 3.85 | | Good | 3 | 11.54 | | Acceptable | 1 | 3.85 |
| C | 2 | 7.69 | | OK | 21 | 80.77 | | Marginal (high) | 2 | 7.69 |
| D | 17 | 65.38 | | Poor | 2 | 7.69 | | Marginal (low) | 19 | 73.08 |
| F | 6 | 23.08 | | | | | | Not acceptable | 4 | 15.38 |

The members' mean SUS score of **54.40** is rated **"OK"**. It falls in the **low-marginal acceptability range** and earns a **grade of D** on the Sauro–Lewis curved scale, below the benchmark average of 68. Scores were tightly grouped: four in five members (80.77%) scored in the "OK" band, and only one (R05, 77.50) reached the acceptable range. Prorating the five partial respondents barely changed the result (54.40 vs 54.05). Per-respondent scores are in `analysis/study6_tables.md`, Table S1.

**Table 8. SUS item responses of the members**

| Item | Statement | Tone | n | Mean (1–5) | % agree (4–5) | Mean contribution (0–4) |
|---|---|---|---:|---:|---:|---:|
| Q1 | I think I would like to use this application frequently. | + | 25 | 4.00 | 76.00 | 3.00 |
| Q2 | I found the application unnecessarily complex. | − | 26 | 3.54 | 50.00 | 1.46 |
| Q3 | I thought the application was easy to use. | + | 24 | 3.83 | 66.67 | 2.83 |
| Q4 | I think that I need the support of a technical person to be able to use this application. | − | 26 | 4.04 | 69.23 | 0.96 |
| Q5 | I found the various functions in the application were well integrated. | + | 26 | 3.92 | 69.23 | 2.92 |
| Q6 | I thought there was too much inconsistency in this application. | − | 26 | 2.96 | 30.77 | 2.04 |
| Q7 | I would imagine that most people would learn this application very quickly. | + | 25 | 3.72 | 68.00 | 2.72 |
| Q8 | I found the application very awkward to use. | − | 25 | 3.20 | 32.00 | 1.80 |
| Q9 | I felt very confident in using the application. | + | 25 | 4.12 | 84.00 | 3.12 |
| Q10 | I needed to learn a lot of things before I could get going with this application. | − | 26 | 4.00 | 65.38 | 1.00 |

Note: for negatively worded (−) items, a *higher* mean (more agreement) means *lower* usability.

**Item-level reading.** Agreement with the positively worded items was high. Members said they **felt confident using the application** (Q9, 84.00% agree), **would like to use it frequently** (Q1, 76.00%), and found its functions **well integrated** (Q5, 69.23%). The score was pulled down mainly by two negatively worded items. About two in three members agreed that they **would need the support of a technical person** (Q4, 69.23%) and **needed to learn a lot before getting going** (Q10, 65.38%). These two items contributed the least to the score (about 1.0 of 4 points each).

**Caveat on the negatively worded items.** The SUS alternates positive and negative statements, and many members agreed with both kinds. The mean agreement was 3.92 for positive items and 3.55 for negative items, so members leaned toward agreement whatever the statement said. Three findings suggest that some respondents may have read the negative items as positive ones, or agreed with them out of habit (acquiescence):
- **The two halves do not move together.** For respondents who answered consistently, a high positive-item score should go with a high reversed negative-item score. Here the mean correlation between them was −0.07.
- **The full SUS has poor internal consistency** (α = 0.42, n = 21). The SUS usually reaches α ≈ 0.90 (Bangor et al., 2008; Sauro & Lewis, 2016).
- **Part 2B was clearly favourable** (Section 2.3), including the ease-of-use items.

Sauro and Lewis (2011) documented this kind of error with alternating-tone questionnaires. It may be stronger here because the respondents are farmers answering a bilingual (English–Cebuano) form, which was not separately validated. On the other hand, the SUS score still correlates moderately and significantly with the Part 2B ease-of-use score (Spearman ρ = 0.45, p = 0.024, n = 25). This means the SUS still ranks respondents in a meaningful way, and the agreement with Q4 and Q10 may also reflect a real need for assistance. Respondent R21, for example, wrote that the app is best for those who are used to phones. The **standard SUS score of 54.40 is therefore reported as the official result**, but it should be read as a **conservative (lower-bound) estimate** of perceived usability. The specific message from Q4 and Q10, that members feel they need help and training, should be taken seriously.

### 2.3 Perceived usefulness, ease of use and intention to use (Part 2B, members)

**Table 9. Part 2B item means of the members**

| Construct | Item | Statement | n | Mean | SD | Verbal interpretation |
|---|---|---|---:|---:|---:|---|
| PU | Q1 | Using the application allows me to place orders more quickly. | 25 | 5.32 | 1.41 | Agree |
| PU | Q2 | Using the application makes it more convenient for me to order products from Baybayani. | 25 | 5.56 | 1.08 | Agree |
| PU | Q3 | Using the application helps me keep track of my orders. | 25 | 5.60 | 1.00 | Agree |
| PU | Q4 | Using the application improves my overall online shopping experience. | 26 | 5.50 | 1.27 | Agree |
| PU | Q5 | I find the application useful for buying products from Baybayani. | 27 | 5.70 | 1.30 | Agree |
| PEOU | Q6 | Learning to use the application was easy for me. | 26 | 5.42 | 1.55 | Agree |
| PEOU | Q7 | I find it easy to find the products I want. | 27 | 5.63 | 1.18 | Agree |
| PEOU | Q8 | I find the ordering and checkout process easy to follow. | 27 | 5.22 | 1.19 | Slightly agree |
| PEOU | Q9 | The user interface of the application is easy to understand. | 25 | 5.00 | 1.38 | Slightly agree |
| PEOU | Q10 | It is easy for me to become skillful at using the application. | 27 | 5.00 | 1.30 | Slightly agree |
| BI | Q11 | I intend to use the application for my future orders. | 25 | 5.32 | 1.52 | Agree |
| BI | Q12 | I prefer ordering through the application over buying in person. | 24 | 5.21 | 1.10 | Slightly agree |
| BI | Q13 | I would recommend the application to other people. | 25 | 5.68 | 1.25 | Agree |

**Table 10. Part 2B construct scores and reliability (members)**

| Construct | Items | n | Mean | SD | Median | Range | Cronbach's α (n) | Verbal interpretation |
|---|---|---:|---:|---:|---:|---|---|---|
| Perceived usefulness | Q1–Q5 | 26 | **5.55** | 0.97 | 5.73 | 3.40–7.00 | 0.86 (24), good | **Agree** |
| Perceived ease of use | Q6–Q10 | 27 | **5.25** | 1.00 | 5.20 | 3.40–6.80 | 0.84 (24), good | **Slightly agree** |
| Intention to use / recommend | Q11–Q13 | 25 | **5.42** | 1.02 | 5.33 | 2.67–7.00 | 0.69 (23), questionable | **Agree** |
| All Part 2B items | Q1–Q13 | 26 | **5.42** | 0.90 | 5.58 | 3.23–6.54 | 0.94 (20), excellent | **Agree** |

**Table 11. Distribution of member construct scores by verbal interpretation, f (%)**

| Interpretation | Usefulness (n = 26) | Ease of use (n = 27) | Intention (n = 25) | Overall (n = 26) |
|---|---:|---:|---:|---:|
| Extremely agree | 7 (26.92) | 7 (25.93) | 5 (20.00) | 6 (23.08) |
| Agree | 9 (34.62) | 6 (22.22) | 12 (48.00) | 11 (42.31) |
| Slightly agree | 6 (23.08) | 7 (25.93) | 4 (16.00) | 4 (15.38) |
| Neutral | 3 (11.54) | 5 (18.52) | 3 (12.00) | 4 (15.38) |
| Slightly disagree | 1 (3.85) | 2 (7.41) | 0 (0.00) | 1 (3.85) |
| Disagree | 0 (0.00) | 0 (0.00) | 1 (4.00) | 0 (0.00) |
| Extremely disagree | 0 (0.00) | 0 (0.00) | 0 (0.00) | 0 (0.00) |

Members **agreed** that the platform is useful, easy to use and worth continuing to use (overall mean 5.42). Perceived usefulness was rated highest (5.55, *agree*). The app was seen as **useful for buying from Baybayani** (Q5, 5.70), **helpful for keeping track of orders** (Q3, 5.60) and **more convenient** (Q2, 5.56). Intention to use was also positive (5.42, *agree*): members were most willing to **recommend the app to others** (Q13, 5.68), and somewhat less sure that they **prefer the app to buying in person** (Q12, 5.21, *slightly agree*). Perceived ease of use was the lowest construct (5.25, *slightly agree*). Finding products was rated easy (Q7, 5.63), but the **user interface** (Q9, 5.00), **becoming skillful** (Q10, 5.00) and the **ordering and checkout process** (Q8, 5.22) were rated only *slightly agree*. This matches the SUS finding that members feel they need more learning and support. Most members scored in the *agree* or *extremely agree* range on usefulness (61.54%) and intention (68.00%), and nearly half did on ease of use (48.15%) (Table 11). Only one or two respondents per construct scored below neutral.

Reliability was **good** for usefulness and ease of use, **excellent** for all 13 items together, and **questionable but close to acceptable** for the three-item intention scale (α = 0.69). Short scales usually have lower alpha. Two members (R04, R05) gave the same answer (6) to all 13 items. This straight-lining pattern should be kept in mind, although it does not change the interpretation.

### 2.4 Administrator evaluation (R01, n = 1)

There was only one administrator, so these results are descriptive. They show the view of the person who uses the back-office features, not a group estimate.

**Table 12. Administrator's SUS responses (Part 1A)**

| Item | Statement | Response (1–5) | Contribution (0–4) |
|---|---|---:|---:|
| Q1 | I think I would like to use this application frequently. | 5 | 4 |
| Q2 | I found the application unnecessarily complex. | 4 | 1 |
| Q3 | I thought the application was easy to use. | 5 | 4 |
| Q4 | I think that I need the support of a technical person to be able to use this application. | 1 | 4 |
| Q5 | I found the various functions in the application were well integrated. | 4 | 3 |
| Q6 | I thought there was too much inconsistency in this application. | 2 | 3 |
| Q7 | I would imagine that most people would learn this application very quickly. | 4 | 3 |
| Q8 | I found the application very awkward to use. | 1 | 4 |
| Q9 | I felt very confident in using the application. | 4 | 3 |
| Q10 | I needed to learn a lot of things before I could get going with this application. | 1 | 4 |
| | **SUS score** | | **82.5** |

**Table 13. Administrator's responses to Part 1B (1–7)**

| Construct | Item | Statement | Response | Verbal interpretation |
|---|---|---|---:|---|
| PU | Q1 | Using the application helps me record orders more accurately. | 7 | Extremely agree |
| PU | Q2 | Using the application allows me to manage orders more quickly. | 7 | Extremely agree |
| PU | Q3 | Using the application makes retrieving order records easier. | 7 | Extremely agree |
| PU | Q4 | Using the application helps me generate order reports and summaries. | 7 | Extremely agree |
| PU | Q5 | I find the application useful for performing my tasks. | 7 | Extremely agree |
| PEOU | Q6 | Learning to use the administrator features was easy for me. | 6 | Agree |
| PEOU | Q7 | I find it easy to view and update order information. | 7 | Extremely agree |
| PEOU | Q8 | The administrator interface is clear and understandable. | 7 | Extremely agree |
| PEOU | Q9 | Interacting with the application requires little mental effort. | 2 | Disagree |
| PEOU | Q10 | It is easy for me to get the application to do what I need it to do. | 6 | Agree |
| BI | Q11 | I intend to continue using the application for tracking the organization's orders. | 7 | Extremely agree |
| BI | Q12 | I prefer using the application over my current method of recording orders. | 6 | Agree |
| BI | Q13 | I would recommend the continued use of the application in the organization. | 7 | Extremely agree |
| | | **Perceived usefulness (mean of Q1–Q5)** | **7.00** | **Extremely agree** |
| | | **Perceived ease of use (mean of Q6–Q10)** | **5.60** | **Agree** |
| | | **Intention to use (mean of Q11–Q13)** | **6.67** | **Extremely agree** |
| | | **All 13 items** | **6.38** | **Extremely agree** |

The administrator's SUS score of **82.5** is rated **"Excellent"**, is **acceptable**, and earns a **grade of A** (90th–95th percentile). The administrator's answers to the reversed items were consistent with the positive ones: they did not need technical support (Q4 = 1) and did not need to learn a lot first (Q10 = 1). The administrator rated the order-management features **extremely useful**: recording, managing, retrieving and reporting orders all received 7. They **intend to keep using** the system and recommend it for the organization. There were two reservations. The administrator agreed that the application is **"unnecessarily complex"** (SUS Q2 = 4) and **disagreed that using it requires little mental effort** (1B-Q9 = 2). Even though the administrator found the interface clear, the back-office work takes noticeable effort. Simplifying the frequent administrator tasks is a reasonable next step.

### 2.5 Comments and suggestions

Eight of the 28 respondents (the administrator and 7 members) wrote a comment with content. One member wrote "no comment", and 19 left the item blank.

**Table 14. Themes in the comments**

| Theme | Respondents | Summary of what was said |
|---|---|---|
| Satisfaction and endorsement | R04, R21, R22, R23, R26 | Members described themselves as **satisfied** (R04). They called the app **good for buying vegetables more easily** (R26) and **convenient for those used to phones** (R21). Two said they would **strongly recommend it to their friends** (R22, R23; the two comments are almost word for word the same). |
| Requested features: payment | R01 (administrator) | Add **online payment options** such as GCash, Maya and MariBank. |
| Requested features: order handling | R20 | Show the **customer's address** and a **pick-up time**, so the store can prepare and prioritize orders. |
| General improvement | R26 | The app is good, but **this kind of app still needs to be improved**. |
| Beyond the app | R11 (officer) | **Promote value-adding of vegetable products.** This concerns the organization's products rather than the software. |

The comments were few but mostly positive, and they agree with the Part 2B results. The concrete suggestions are about **transactions and logistics**: e-wallet payment, delivery address and pick-up scheduling. R21's remark that the app suits "those who are used to phones" supports the SUS finding that some members, especially those less used to smartphones, may need help to use the platform.

---

## 3. Summary of findings

1. **Respondents.** The 27 member-respondents were mostly male (70.37%) rank-and-file members (88.89%), who had been with Baybayani for about two years (mean 2.01). Their main crops were eggplant, bitter gourd and cucumber. All who answered had pest problems, and most also had plant disease. Most reported a farm income of ₱100,000 or less a year (median ₱82,500).
2. **Usability (SUS).** Members gave a mean SUS of **54.40 (SD 7.93)**, rated **"OK"**, *marginal (low)* in acceptability, grade **D**. The score is held down by agreement with "I would need technical support" and "I needed to learn a lot". Because of the inconsistent answers to the reversed items (α = 0.42), this score is best read as a conservative estimate.
3. **Usefulness, ease of use and intention (Part 2B).** Members **agreed** that the platform is useful (**5.55**) and that they intend to use and recommend it (**5.42**). They **slightly agreed** that it is easy to use (**5.25**). The overall mean was **5.42 (agree)**, and the 13 items were highly reliable (α = 0.94). Ease of use was the weakest construct, especially the user interface, becoming skillful and the checkout process.
4. **Administrator.** The administrator rated usability **Excellent (SUS 82.5, grade A)** and the order-management features **extremely useful (7.00)**, with a strong intention to keep using the system (6.67). The administrator noted that the system is somewhat complex and takes mental effort.
5. **Comments.** The comments mostly endorsed the app. The requests were for e-wallet payment and for showing the customer address and pick-up time.

## 4. Implications and recommendations

These follow from the results. They are offered for the project's consideration.

- **Train and support members.** The clearest weak point is that members feel they need help and a lot of learning (SUS Q4, Q10; Part 2B Q9, Q10). Hands-on orientation sessions, a short illustrated Cebuano guide, and a named go-to person (such as an officer) could address this.
- **Simplify ordering and checkout,** and review the interface wording in Cebuano (Part 2B Q8, Q9).
- **Add the requested features:** e-wallet payment (GCash, Maya, MariBank), the customer's delivery address, and pick-up time scheduling for order preparation.
- **Reduce the administrator's workload** by streamlining the frequent order tasks (SUS Q2; Part 1B Q9).
- **For later evaluations,** consider using the all-positive version of the SUS (Sauro & Lewis, 2011) or reading the items aloud in Cebuano. This would reduce errors on the reversed items among farmer-respondents.

## 5. Limitations

- The members were a convenience sample (n = 27, with 26 SUS scores), and there was only one administrator. The results describe this group and are not tested inferentially beyond the reliability and correlation checks.
- The SUS had low internal consistency in this sample (Section 2.2), so the member SUS score should be read together with Part 2B.
- Responses were self-reported on the day of the evaluation. Income and years as member are respondents' estimates, and a third of the members did not report income.
- Two members (R04, R05) gave the same answer to every Part 2B item, and two members' comments were nearly identical. These may reflect respondents influencing each other or answering quickly.

## References

Bangor, A., Kortum, P. T., & Miller, J. T. (2008). An empirical evaluation of the System Usability Scale. *International Journal of Human–Computer Interaction, 24*(6), 574–594.

Bangor, A., Kortum, P., & Miller, J. (2009). Determining what individual SUS scores mean: Adding an adjective rating scale. *Journal of Usability Studies, 4*(3), 114–123.

Brooke, J. (1996). SUS: A "quick and dirty" usability scale. In P. W. Jordan, B. Thomas, B. A. Weerdmeester, & I. L. McClelland (Eds.), *Usability evaluation in industry* (pp. 189–194). Taylor & Francis.

Davis, F. D. (1989). Perceived usefulness, perceived ease of use, and user acceptance of information technology. *MIS Quarterly, 13*(3), 319–340.

George, D., & Mallery, P. (2003). *SPSS for Windows step by step: A simple guide and reference, 11.0 update* (4th ed.). Allyn & Bacon.

Sauro, J., & Lewis, J. R. (2011). When designing usability questionnaires, does it hurt to be positive? *Proceedings of the SIGCHI Conference on Human Factors in Computing Systems (CHI '11)*, 2215–2224.

Sauro, J., & Lewis, J. R. (2016). *Quantifying the user experience: Practical statistics for user research* (2nd ed.). Morgan Kaufmann.
