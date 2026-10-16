# Documentation

This folder holds the printable documents for the **Baybayani** evaluation under the
VSU research project *Farm to Table: A Management Information System for Farmers and
Food Business Establishments in Baybay City, Leyte* (Project Code DCST.0824-0825).

The documents are written in LaTeX so that they print the same way from any
computer. This page explains how to set up LaTeX the first time you clone the
repository on a new computer, and how to rebuild the PDFs.

## Contents

| Path | What it is |
| ---- | ---------- |
| `evaluation-instrument/user-instrument-iso25019.tex` | **User evaluation instrument**: quality in use, based on ISO/IEC 25019:2023. For customers and farmer-group administrators who were not part of the development. English with Cebuano translation. |
| `evaluation-instrument/technical-instrument-iso25010.tex` | **Technical evaluation instrument**: product quality, based on ISO/IEC 25010:2023. For developers, testers and system architects. |
| `evaluation-instrument/study-info.tex` | Project title, project code and researchers. Both instruments read these from this one file. |
| `evaluation-instrument/instrument.sty` | Shared layout: A4 page, VSU header, rating tables, check boxes, comment boxes. |
| `evaluation-instrument/assets/vsu-logo.png` | VSU logo used in the header. |

### How the instruments are organized

Both instruments have the same four parts:

1. **Informed consent and data privacy notice** (RA 10173), with a signature line.
   This page is filed separately from the answers; the two are linked only by the
   respondent number in the page header.
2. **Respondent (or evaluator) profile.**
3. **Rating items** on a 5-point scale (5 Strongly Agree to 1 Strongly Disagree),
   grouped by characteristic and subcharacteristic, with a comments box after each
   characteristic.
4. **Open-ended questions.**

| Instrument | Characteristics and subcharacteristics | Items |
| ---------- | -------------------------------------- | ----- |
| User (ISO/IEC 25019:2023) | Beneficialness (usability, accessibility, suitability); Freedom from risk (economic, health, human life, environmental and societal); Acceptability (experience, trustworthiness, compliance) | Part III-A, all respondents: 32 (A1–A32). Part III-B, customers: 10 (B1–B10). Part III-C, administrators: 12 (C1–C12). |
| Technical (ISO/IEC 25010:2023) | Functional suitability, performance efficiency, compatibility, interaction capability, reliability, security, maintainability, flexibility, safety (all 40 subcharacteristics) | 49 (1–49) |

The mean range printed with the scale (4.21–5.00 Strongly Agree, 3.41–4.20 Agree,
2.61–3.40 Neutral, 1.81–2.60 Disagree, 1.00–1.80 Strongly Disagree) is used to
interpret the mean scores.

---

## First-time setup

You need a **TeX distribution** (the program that turns `.tex` into `.pdf`). An
editor is optional; any text editor works.

### Windows: MiKTeX (recommended)

1. Download the installer from <https://miktex.org/download> and run it.
   - Choose **Install only for me** unless you have admin rights and want it for all users.
   - At **Install missing packages on-the-fly**, choose **Yes** (or *Ask me*).
     MiKTeX then downloads any package a document needs the first time it is built.
2. Open **MiKTeX Console** → **Updates** → **Check for updates** → **Update now**.
   A fresh install is often out of date.
3. Close and reopen any terminal, then check that it works:

   ```bash
   pdflatex --version
   ```

`latexmk` (the one-command build below) is a Perl script. MiKTeX includes it but
not Perl. If `latexmk` reports that Perl is missing, either install
[Strawberry Perl](https://strawberryperl.com/) or use the plain `pdflatex`
commands instead. Git Bash from [Git for Windows](https://git-scm.com/) already
includes Perl, so `latexmk` works there.

*Alternative:* TeX Live for Windows (<https://tug.org/texlive/windows.html>) is a
larger, all-in-one install that includes Perl.

### macOS: MacTeX

1. Download and install MacTeX from <https://tug.org/mactex/> (about 5 GB; includes
   everything used here). For a smaller install, use BasicTeX and add the packages
   listed in [Required LaTeX packages](#required-latex-packages):

   ```bash
   sudo tlmgr update --self
   ```

   ```bash
   sudo tlmgr install latexmk needspace lastpage enumitem fancyhdr colortbl xcolor helvetic psnfss
   ```

2. Open a new Terminal and check: `pdflatex --version`.

### Linux: TeX Live

Debian or Ubuntu:

```bash
sudo apt install texlive-latex-base texlive-latex-recommended texlive-latex-extra texlive-fonts-recommended latexmk
```

Fedora:

```bash
sudo dnf install texlive-scheme-medium latexmk
```

### Optional editor: Visual Studio Code

Install the **LaTeX Workshop** extension (James Yu). Open a `.tex` file and save it;
the extension builds the PDF and shows it beside the source. It uses `latexmk`,
so on Windows make sure Perl is available (see above).

---

## Building the PDFs

Run these from the `docs/evaluation-instrument` folder. The `.tex` files load
`study-info.tex`, `instrument.sty` and `assets/` by relative path, so the build has
to start in that folder.

```bash
cd docs/evaluation-instrument
```

**With latexmk** (runs LaTeX as many times as needed):

```bash
latexmk -pdf user-instrument-iso25019.tex technical-instrument-iso25010.tex
```

**Without latexmk**, run `pdflatex` twice per file. The second run fills in the
"Page *x* of *y*" totals.

```bash
pdflatex user-instrument-iso25019.tex
```

```bash
pdflatex technical-instrument-iso25010.tex
```

Then run both commands again.

The PDFs appear next to the `.tex` files. To remove the build by-products
(`.aux`, `.log`, `.out`, …):

```bash
latexmk -c
```

### Required LaTeX packages

All are standard and come with MiKTeX and full TeX Live. MiKTeX installs any that
are missing on the first build if on-the-fly installation is on.

`geometry`, `fontenc`, `inputenc`, `helvet` (psnfss), `graphicx`, `array`,
`longtable`, `tabularx`, `xcolor` with `colortbl`, `enumitem`, `fancyhdr`,
`lastpage`, `needspace`, `calc`, `amssymb`.

---

## Editing the instruments

- **Project title, code or researchers:** edit `evaluation-instrument/study-info.tex`
  and rebuild. Both instruments change together.
- **Rating items:** each item is one line in the `.tex` file.
  - User instrument: `\BiItem{English statement}{Cebuano translation}`
  - Technical instrument: `\EnItem{Statement}`
  - Items are numbered automatically; the numbering restarts at each
    `\StartNumbering{A}` (or `B`, `C`).
  - A shaded subcharacteristic row is `\SubChar{...}`; a characteristic heading
    with its definition is `\Characteristic{...}{...}`.
- **Special characters** must be escaped in LaTeX: `\&`, `\%`, `\$`, `\#`, `\_`.
- The Cebuano translations should be reviewed by a native speaker before the
  instruments are printed for respondents.

## Printing

- Paper: **A4**. In the print dialog, choose **Actual size** (or 100%), not
  *Fit to page*, so the rating circles and writing lines keep their size.
- Print **single-sided** so the consent page (page 1) can be separated from the
  answers.
- Write the same respondent number on every page of a set before handing it out.

## Troubleshooting

| Problem | Fix |
| ------- | --- |
| `File 'study-info.tex' not found` or `instrument.sty not found` | Build from inside `docs/evaluation-instrument`, not from the repository root. |
| `File 'xxx.sty' not found` | MiKTeX: open MiKTeX Console → Packages, search for the package and install it, or turn on on-the-fly installation. TeX Live: `tlmgr install <package>`. |
| `latexmk: perl not found` (Windows) | Install Strawberry Perl, use Git Bash, or build with `pdflatex` (twice). |
| Footer shows "Page 1 of ??" | Run `pdflatex` a second time. |
| Build stops at a `?` prompt | Type `x` and press Enter, read the first `!` error in the `.log` file, then fix that line. |
