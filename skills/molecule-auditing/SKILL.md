---
name: molecule-auditing
description: >
  Audit small molecules from an Ersilia screening run and prioritise them for drug discovery.
  Use this skill whenever the user has a CSV file from Ersilia model outputs and wants to rank,
  score, or filter molecules based on activity, drug-likeness, or ADMET properties. Also trigger
  when the user asks to evaluate candidates from a screening, understand what the Ersilia scores
  mean, identify promising compounds, prepare a hit list for follow-up, or find novel vs known-like
  antibiotic candidates. Even if the user just says "can you look at these molecules" and they
  provide a CSV with model output columns, this skill is the right tool.
argument-hint: <molecules-path> [--context <disease-or-target>] [--mode similar|novel] [--output <path>]
allowed-tools: [Read, Bash, Write, WebFetch, AskUserQuestion]
---

# Molecule Auditing

You audit a list of small molecules from an Ersilia screening run and produce a prioritised report. Your value is connecting raw model scores to meaningful drug discovery criteria — helping researchers decide which molecules to advance, flag, or set aside.

Input files can be large (1000+ molecules). **Never read the full CSV into your context.** Instead, inspect only the headers to detect model IDs, fetch metadata from GitHub, then delegate all row-level processing to `scripts/process_molecules.py`. You read only the compact JSON summary that script produces.

## Parse Arguments

- `<molecules-path>` (required): CSV file with molecule data and Ersilia model output columns
- `--context <disease-or-target>` (optional): Therapeutic context, e.g. `"malaria"`, `"M. tuberculosis"`, `"hERG inhibition"`. Shapes how results are framed and adjusts thresholds (CNS targets get stricter rules).
- `--mode <similar|novel>` (optional): Structural novelty mode for antibiotic campaigns.
  - `similar`: favour compounds resembling known antibiotics (lead optimisation, known mechanism)
  - `novel`: favour compounds structurally distinct from known antibiotics (first-in-class, avoids class-level resistance). For neglected tropical diseases, this is often the more scientifically interesting mode.
  - When `--mode` is given, the script uses Tanimoto similarity against `assets/antibiotic_reference.csv` (requires RDKit). See `references/antibiotic-criteria.md` for context.
- `--output <path>` (optional): Output path for the audit report. Defaults to `audit_report.md` beside the input file.

---

## Step 1: Read Headers Only

Use `Bash` to read just the header row — do **not** load the full file:

```bash
head -1 <molecules-path>
```

From the headers, identify:
- **SMILES column**: `input` or `smiles` (case-insensitive)
- **Key column**: `key`
- **Score columns**: everything else. For each, check whether it matches `{feature}.{model_id}` where the suffix looks like `eos` + 4 alphanumeric chars (e.g. `inhibition_50um.eos4e40`).

Note the unique model IDs found and how many columns each contributes.

---

## Step 2: Fetch Model Metadata from GitHub

For each unique model ID, fetch two files using `WebFetch`. No CLI or library needed — plain HTTP.

See `references/ersilia-metadata-guide.md` for exact URL patterns and parsing guidance.

For each model, extract:
- **From `run_columns.csv`**: per-column `name`, `direction`, `description`
- **From `metadata.json`**: `Title`, `Interpretation`, `Biomedical Area`, `Target Organism`, `Task`, `Subtask`

### Building the column metadata JSON

Save column metadata to a temp JSON file (e.g. `/tmp/col_meta_<timestamp>.json`).

**For each column, you must determine two fields beyond what the raw metadata provides:**

**`want_high` (boolean or null):** Does a higher value of this column's concept benefit drug discovery? This is NOT the same as `direction`. Reason from the description and model interpretation:
- Inhibition/activity/potency probability → `true` (we want more activity)
- Toxicity, mutagenicity, hERG blockade, carcinogenicity, DILI, Ames → `false` (we want less of these)
- Solubility probability, bioavailability, absorption, permeability → `true` (we want more)
- Molecular weight, LogP, TPSA, rotatable bonds → `null` (range-filtered via Lipinski/Veber, not scored directionally)
- Featurisation outputs (embeddings, fingerprints) → `null`

**`scoring_role` (string):** How the script uses this column:
- `"efficacy"`: primary activity/potency measure from an Activity-prediction model → used for the aggregate ranking score
- `"safety_flag"`: toxicity or safety concern probability → flagged when value > `flag_threshold` (set `flag_threshold: 0.5` for probability outputs)
- `"beneficial_admet"`: positive ADMET property (bioavailability, absorption) → noted but not mixed into the aggregate score
- `"physicochemical"`: MW, LogP, TPSA, etc. → handled via Lipinski/Veber rules, not scored
- `"info"`: featurisation or other non-directional output → excluded from scoring

The `Task`/`Subtask` fields from `metadata.json` help determine role: "Activity prediction" → `efficacy`; "Property calculation" → likely `physicochemical`, `safety_flag`, or `beneficial_admet` depending on the concept.

**Example output:**

```json
{
  "inhibition_50um.eos4e40": {
    "direction": "high",
    "want_high": true,
    "scoring_role": "efficacy",
    "flag_threshold": null,
    "description": "Probability of inhibiting E.coli growth at 50 uM",
    "model_title": "Broad spectrum antibiotic activity",
    "model_interpretation": "Probability that a compound inhibits E.coli growth...",
    "task": "Activity prediction"
  },
  "ames.eos7m30": {
    "direction": "high",
    "want_high": false,
    "scoring_role": "safety_flag",
    "flag_threshold": 0.5,
    "description": "Predicted probability of Ames mutagenicity",
    "model_title": "ADMET Calculator",
    "model_interpretation": "...",
    "task": "Property calculation"
  },
  "molecular_weight.eos7m30": {
    "direction": "high",
    "want_high": null,
    "scoring_role": "physicochemical",
    "flag_threshold": null,
    "description": "Physicochemical property for molecular weight",
    "model_title": "ADMET Calculator",
    "model_interpretation": "...",
    "task": "Property calculation"
  },
  "bioavailability_ma.eos7m30": {
    "direction": "high",
    "want_high": true,
    "scoring_role": "beneficial_admet",
    "flag_threshold": null,
    "description": "Predicted probability of oral bioavailability",
    "model_title": "ADMET Calculator",
    "model_interpretation": "...",
    "task": "Property calculation"
  }
}
```

If a fetch fails, include the column with `"want_high": null, "scoring_role": "info"` so the script can still run.

---

## Step 3: Run the Processing Script

Run `scripts/process_molecules.py` via `Bash`. The script reads the full CSV, scores all molecules using **only `scoring_role == "efficacy"` columns**, flags safety concerns from `scoring_role == "safety_flag"` columns, and writes a compact JSON summary.

```bash
python <skill_dir>/scripts/process_molecules.py \
  <molecules-path> \
  --metadata /tmp/col_meta_<timestamp>.json \
  --top-n 30 \
  --context "<context_string>" \
  [--mode similar|novel] \
  [--skill-dir <skill_dir>] \
  --output-dir <output_dir>
```

`<skill_dir>` is the directory containing this SKILL.md file. Include `--mode` and `--skill-dir` only when `--mode` was requested by the user.

The script prints its output path and a one-line count summary. Read the resulting `audit_summary.json` file — it contains:

- Total molecule count, classification breakdown (Promising / Borderline / Deprioritise)
- Score distribution across the full set (from efficacy columns only)
- Top 30 candidates with scores, safety flags, and classification
- Novelty stats (only when `--mode` is set): how many compounds are structurally novel vs similar to known antibiotics
- Caveats (RDKit availability, unknown columns, no efficacy columns detected)

---

## Step 4: Write the Audit Report

Using the `audit_summary.json` and the model metadata you already have in context, write the Markdown report. The report has two parts: a **Dataset Overview** preamble (accessible to non-expert collaborators and funders) followed by the **Audit Results** (for the researcher running the screen).

**Full report structure:**

```markdown
# Molecule Audit Report

---

## Dataset Overview

> This section describes the data and the models used. It is written to be
> readable without prior knowledge of Ersilia or cheminformatics.

**What is this file?**
One or two sentences: N molecules evaluated by M computational models via
the Ersilia Model Hub. Each row is one molecule; each column is a model
prediction. The goal is to identify the most promising candidates for
<context or "drug discovery">.

### Models Used

For each unique model in the CSV, write a subsection:

#### <Model Title> (`<model_id>`)
- **What it predicts**: plain-English description of the model's output
  (cite the `Interpretation` field from metadata.json verbatim or paraphrase it)
- **Trained on**: organism, assay, dataset (from `Target Organism`, `Biomedical Area`)
- **Publication**: link from metadata.json if available
- **Output columns**: list each column with a one-line plain description
- **Key limitation**: one honest caveat about when predictions may be unreliable
  (e.g., "trained on E.coli only; extrapolation to other organisms is uncertain")

### Column Guide

A table covering every score column (use `column_stats` from audit_summary.json
to know which columns exist). Write it for a biologist who has never seen the
Ersilia platform. Use `description` and `scoring_role` from column metadata.

| Column (decoded) | Model | What it measures | A high value means… | A low value means… |
|---|---|---|---|---|
| Antibiotic activity (`inhibition_50um`) | eos4e40 | Probability of E.coli growth inhibition | Likely active against E.coli | Probably inactive |
| Mutagenicity risk (`ames`) | eos7m30 | Probability of DNA mutagenicity | Safety concern — may damage DNA | Low mutagenicity risk |
| ... | ... | ... | ... | ... |

Group columns by model. For safety columns, make the "high value = concern"
language explicit. For physicochemical columns (MW, LogP) explain the
Lipinski range rather than a directional answer.

### Score Distributions

A table of per-column statistics from `column_stats` in audit_summary.json.
Include all columns with a defined scoring_role (skip "info" columns).
For safety_flag columns, include the "% flagged" column.

| Column | Min | Median | 75th pct | Max | % above threshold |
|---|---|---|---|---|---|
| inhibition_50um (efficacy) | 0.001 | 0.012 | 0.042 | 0.996 | — |
| ames (safety) | 0.01 | 0.31 | 0.55 | 0.99 | 34% > 0.5 |
| herg (safety) | ... | ... | ... | ... | 41% > 0.5 |
| qed (drug-likeness) | ... | ... | ... | ... | — |

After the table, add 1–2 sentences interpreting what the distributions mean:
e.g. "Most molecules have low antibiotic activity scores, consistent with a
typical diversity library. Over a third flag as potentially mutagenic — this
is common in unfiltered compound libraries and does not indicate a problem
with the screen."

### Illustrative Top Molecules

Show the top 3 molecules by activity score as worked examples.
For each: key, SMILES (truncated if >40 chars), activity score, top 2–3 other
notable values (e.g. AMES, DILI, QED), classification, and a one-sentence
plain-English summary of why it ranks here.

| Key | Activity | Mutagenicity | DILI | Drug-likeness | Classification | Notes |
|---|---|---|---|---|---|---|
| abc123 | 0.996 | 0.63 ⚠️ | 0.92 ⚠️ | 0.41 | Borderline | Highly active but carries mutagenicity and liver toxicity flags |
| def456 | 0.987 | 0.12 | 0.22 | 0.71 | Promising | Strong activity with clean safety profile — top candidate |

---

## Audit Results

### Overview
- **Input**: <filename>, <N> molecules
- **Context**: <context or "not specified">
- **Mode**: <similar / novel / not set>
- **Scoring**: ranked by <efficacy column(s)>
- **Results**: N Promising | N Borderline | N Deprioritise

### Top Candidates
For each of the top 3–5 Promising molecules: SMILES or key, activity score,
what the score means, any safety flags. Concise but informative — a medicinal
chemist should understand at a glance why each is highlighted.

### Audit Table
Top 30 scored molecules:
Key | SMILES | Activity score | Safety flags | Novelty | Classification
(Include Novelty column only when --mode is set)

### Score Distribution
How spread out are the activity scores, where are the Promising/Borderline
boundaries, any notable clusters.

### Novelty Notes (only when --mode is set)
If mode=novel: highlight structurally novel Promising candidates and explain
what novelty means scientifically (avoids class-level resistance, first-in-class).
If mode=similar: note which candidates resemble known antibiotic classes.
Read references/antibiotic-criteria.md for the full reasoning.

### Safety Profile
- Which safety columns raised the most flags across the full set?
- What fraction of top candidates have ≥1 safety flag?
- Any molecule with 3+ safety flags should be highlighted explicitly.

### Caveats
- RDKit unavailable → Lipinski/PAINS/novelty not computed
- Columns that could not be fetched from GitHub
- Columns without a recognised model ID suffix
- No efficacy columns detected → scoring not possible
- --mode requested but RDKit unavailable → Tanimoto not computed
```

Save to `--output` path or default `audit_report.md`.

---

## Handling Edge Cases

- **No efficacy columns detected**: If no column has `scoring_role == "efficacy"`, the aggregate score cannot be computed. Ask the user which model(s) represent primary activity, or fall back to using all direction-aware columns as a proxy (and note this clearly).
- **No model IDs in columns**: If no column matches the `{feature}.{model_id}` pattern, ask the user which Ersilia model(s) produced the file, or proceed without metadata and note the limitation.
- **Script fails**: Read the error message, diagnose it (missing pandas? wrong column format?), and fix or report clearly.
- **--mode without RDKit**: Note in caveats that Tanimoto similarity could not be computed; run without novelty scoring.
