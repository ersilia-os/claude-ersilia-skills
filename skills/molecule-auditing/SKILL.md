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

This is a **pre-deliverable audit**: the skill assumes the user has already done their virtual-screening homework (activity prediction, drug-likeness, diversity, earlier triage) and is now bringing a curated shortlist for final scoring. It is not a tool for processing raw screening libraries.

Input files can contain hundreds of molecules. **Never read the full CSV into your context.** Instead, inspect only the headers to detect model IDs, fetch metadata from GitHub, then delegate all row-level processing to `scripts/process_molecules.py`. You read only the compact JSON summary that script produces.

**Hard limit: this skill refuses to process inputs with more than 1000 molecules.** Users with larger sets must prefilter, not chunk. See Step 1 below.

## Parse Arguments

- `<molecules-path>` (required): CSV file with molecule data and Ersilia model output columns
- `--context <disease-or-target>` (optional): Therapeutic context, e.g. `"malaria"`, `"M. tuberculosis"`, `"hERG inhibition"`. Shapes how results are framed and adjusts thresholds (CNS targets get stricter rules).
- `--mode <similar|novel>` (optional): Structural novelty mode for antibiotic campaigns.
  - `similar`: favour compounds resembling known antibiotics (lead optimisation, known mechanism)
  - `novel`: favour compounds structurally distinct from known antibiotics (first-in-class, avoids class-level resistance). For neglected tropical diseases, this is often the more scientifically interesting mode.
  - When `--mode` is given, the script uses Tanimoto similarity against `assets/antibiotic_reference.csv` (requires RDKit). See `references/antibiotic-criteria.md` for context.
- `--output <path>` (optional): Output path for the audit report. Defaults to `audit_report.md` beside the input file.

---

## Step 1: Check Size, Then Read Headers Only

First, count the rows to enforce the 1000-molecule limit. Use `Bash`:

```bash
wc -l <molecules-path>
```

The molecule count is `(line count) - 1` (header row). **If this exceeds 1000, stop immediately.** Do not fetch metadata, do not run the script. Tell the user the file has N molecules and that this skill is a **pre-deliverable audit** for late-stage virtual screening — it expects an already-narrowed candidate set. They need to prefilter their library (by activity, drug-likeness, diversity, or any earlier-stage triage) down to ≤ 1000 molecules before running it. Do **not** suggest splitting the file into chunks: chunking hides the prefiltering work and the scoring is only meaningful on a curated shortlist.

Only if the count is ≤ 1000, read the header row — do **not** load the full file:

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

See `references/ersilia-metadata-guide.md` for exact URL patterns and parsing guidance. See `references/ersilia-model-hub-guide.md` for the higher-level reporting contract (filtering-utility buckets, hard rule that `informational` / `ambiguous` columns are never filterable) and the model-recommendation flow used in Step 4.

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

For the chemistry rules the script applies (Lipinski, Veber, CNS envelope, PAINS and other structural alerts) and their per-context exceptions (CNS, antibiotic, IV/topical, macrocycle/PROTAC/natural product), consult `references/drug-discovery-criteria.md`.

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

### Ersilia columns used
Show, for every Ersilia output column detected, which **filtering-utility bucket** it
falls into and how the audit used it. Buckets and rules are defined in
`references/ersilia-model-hub-guide.md` §Scenario A. The buckets map onto the
`scoring_role` field from Step 2 — this table makes the mapping visible to the reader.

| Column | eos ID | Bucket | Role in this audit |
|---|---|---|---|
| `inhibition_50um.eos4e40` | `eos4e40` | `filterable_quantitative` | Primary efficacy — drives ranking |
| `ames.eos7m30` | `eos7m30` | `filterable_flag` | Safety flag — drops molecules with prob > 0.5 |
| `logp.eos7m30` | `eos7m30` | `range_constrained` | Lipinski filter (≤ 5) |
| `embedding_*.eos…` | `eos…` | `informational` | Not used for filtering; available for clustering |
| `…` (fetch failed) | `eos…` | `ambiguous` | Listed in Caveats; not used for filtering |

Hard rule: only `filterable_quantitative`, `filterable_flag`, and `range_constrained`
columns may enter the score or a filter. `informational` and `ambiguous` columns
appear here for transparency but never drove any decision.

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

### Recommended additional Ersilia models
Identify coverage gaps across three categories — **ADMET / physicochemical**,
**antimicrobial activity** (matched to `--context` and target organisms inferred
from the dataset), and **safety / toxicity flags** — and recommend 1–3 specific
Ersilia models per uncovered category. Use the curated starting set in
`references/ersilia-model-hub-guide.md` §Scenario B; fall back to the Airtable
live lookup documented there when the curated set is insufficient. If a category
is already fully covered by columns in the dataset, keep the heading and say
_"Already covered"_ with the covering eos ID(s) — do not silently omit.

Format per recommendation: ``[`eosXXXX`](https://github.com/ersilia-os/eosXXXX) — what it predicts. Why it fits this dataset. Caveats (if any).``

#### ADMET / physicochemical
- [`eos2lqb`](https://github.com/ersilia-os/eos2lqb) — Probability of high oral bioavailability. The dataset has activity and safety coverage but no absorption signal; this would help prioritise orally-deliverable hits.

#### Antimicrobial activity
- _Already covered_ — `eos9ivc` (antituberculosis activity) is present.

#### Safety / toxicity
- [`eos4tcc`](https://github.com/ersilia-os/eos4tcc) — Probability of hERG channel blockade. None of the existing columns flag cardiac liability.
- [`eos5gge`](https://github.com/ersilia-os/eos5gge) — DILI prediction. Complements hERG for a minimum safety triage.

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
