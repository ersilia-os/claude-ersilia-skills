# Ersilia Model Hub Guide (for molecule auditing)

This guide complements `ersilia-metadata-guide.md`. That file documents the per-model **mechanics** (URLs, JSON/CSV schemas, the `direction` vs `want_high` distinction, the `scoring_role` taxonomy). This file documents the **judgment** layered on top of those mechanics:

- **Scenario A** — the dataset already contains Ersilia model output columns. Decide which columns are useful for filtering and which are not, and show that decision in the audit report.
- **Scenario B** — propose additional Ersilia models that would meaningfully augment the dataset, and recommend them in the audit report.

Both scenarios depend on knowing each model's metadata. Always start by following the fetch workflow in `ersilia-metadata-guide.md`.

---

## What Ersilia is (in one paragraph)

The [Ersilia Model Hub](https://github.com/ersilia-os/ersilia) is an open-source library of pre-trained AI/ML models for infectious-disease and neglected-disease drug discovery (antimicrobial activity, ADMET, toxicity, generative chemistry, molecular representations). Each model lives in its own GitHub repository under the `ersilia-os` organisation with a stable `eos[0-9a-z]{4}` identifier, and the full hub catalogue is maintained in an Airtable base (see §Live lookup below). Models are designed to consume SMILES strings and emit either a score, a value, or a richer object — the column conventions are documented in `ersilia-metadata-guide.md`.

---

## Scenario A — Interpreting Ersilia columns already in the dataset

The classification rules — what a column is *for*, whether it is `efficacy` / `safety_flag` / `beneficial_admet` / `physicochemical` / `info`, and whether `want_high` is `true` / `false` / `null` — are already specified in `ersilia-metadata-guide.md` (see its §"Scoring Role and Desirability" and §"Common Ersilia ADMET column patterns"). Do not duplicate that reasoning here; do it once per column following the existing guide.

What this skill adds is a **reporting contract**: every Ersilia column in the dataset must be visibly accounted for in the audit report so the reader can see which columns drove decisions and which were ignored. Group columns into four **filtering-utility buckets**:

| Bucket | Maps to `scoring_role` | What the audit does with it |
|---|---|---|
| `filterable_quantitative` | `efficacy`, `beneficial_admet` (when `want_high` is set) | Use as a ranking or soft-threshold filter. Show in the Top Candidates table. |
| `filterable_flag` | `safety_flag` | Apply a hard or soft cutoff (default `flag_threshold = 0.5`). Flag offenders in the report. |
| `range_constrained` | `physicochemical` | Apply Lipinski/Veber-style range rules from `drug-discovery-criteria.md`. Do not score directionally. |
| `informational` | `info` (featurisers, embeddings, fingerprints, projections, raw similarities) | **Do not filter on these.** Surface only as context, novelty/clustering input, or in the Column Guide. |
| `ambiguous` | any column where `metadata.json` / `run_columns.csv` could not be fetched, or where `Interpretation` is missing and `want_high` cannot be assigned with confidence | List in the report's Caveats section. Do **not** silently use it as a filter. |

**Hard rule** — A column may only enter the aggregate score or a filtering decision if it falls in `filterable_quantitative`, `filterable_flag`, or `range_constrained`. `informational` and `ambiguous` columns are reportable but never filterable.

---

## Scenario B — Recommending additional Ersilia models

After classifying the columns present, ask: **what is structurally missing from this dataset that an Ersilia model could supply?** Cover three categories, in order:

1. **ADMET / physicochemical properties** — absorption, solubility, permeability, plasma protein binding, metabolic stability, BBB penetration. A screen without any ADMET coverage cannot meaningfully prioritise for downstream development.
2. **Antibiotic / antimicrobial activity** — pathogen-specific activity. Match against the disease context inferred from `--context`, `Target Organism` metadata, or — failing both — the dataset's apparent focus.
3. **Safety / toxicity flags** — hERG, cardiotoxicity, DILI, Tox21, clinical-trial toxicity, adverse drug reactions. A hit list without safety triage is incomplete.

For each category not already covered by the dataset's columns, recommend **1–3 specific Ersilia models** with their eos IDs, drawn from the curated starting set below, or from a live lookup when the curated set is insufficient.

### Curated starting set

Snapshot from the Ersilia Model Hub Airtable on 2026-05-14. Status `Ready`. If a model here looks stale or wrong, fall back to the live lookup (next section).

#### ADMET / physicochemical

| eos ID | Title | What it predicts | `want_high` |
|---|---|---|---|
| `eos7m30` | ADMET properties prediction | Multi-endpoint ADMET (physchem + classification tasks). One-stop ADMET coverage when the dataset has none. | per-column (mixed) |
| `eos2lqb` | Human oral bioavailability | Probability of high oral bioavailability (HOB > 20% / > 50%). | `true` |
| `eos1amr` | Blood-brain barrier penetration | Probability of crossing the BBB. Critical for CNS targets; flag for non-CNS programmes. | context-dependent |
| `eos9tyg` | PAMPA permeability | Probability of being **poorly** permeable (logPeff < 1). Note inverted desirability. | `false` |
| `eos31ve` | Human Liver Microsomal Stability | Probability of being unstable in HLM (t½ ≤ 30 min). | `false` |
| `eos22io` | Plasma Protein Binding | Fraction PPB 0–1. High (> 0.8) reduces free drug. | `false` (usually) |
| `eos9ym3` | MRlogP | Predicted LogP. Range-constrained (Lipinski ≤ 5). | `null` |

#### Antibiotic / antimicrobial activity

| eos ID | Title | Pathogen / scope | `want_high` |
|---|---|---|---|
| `eos4e40` | Broad spectrum antibiotic activity | *E. coli* growth inhibition at 50 µM. | `true` |
| `eos18ie` | *S. aureus* activity | Probability of growth inhibition (80% cut at 50 µM). | `true` |
| `eos3804` | *A. baumannii* growth inhibition | High-priority ESKAPE pathogen. | `true` |
| `eos5xng` | *B. cenocepacia* inhibition | Drug-resistant pathogen, CF-relevant. | `true` |
| `eos9ivc` | Antituberculosis activity | *M. tuberculosis* MIC50/MIC90 inhibition. | `true` |
| `eos46ev` | *M. tuberculosis* inhibitor | M.tb inhibition (IC50 < 5 µM). | `true` |
| `eos4rta` | Antimalarial (MMV) | *P. falciparum* NF54 inhibition. | `true` |
| `eos2gth` | MAIP antimalarial | Antimalarial potential score. | `true` |
| `eos3lyd` | Efflux pump avoidance | Probability of being an efflux evader (gram-negative). Useful as a secondary filter alongside primary activity. | `true` |
| `eos7ike` | eNTRy rules (gram-negative) | Three binary flags for low globularity, low rotatable bonds, primary amine — gram-negative penetration heuristic. | `true` (flags) |
| `eos2xeq` | Similarity to known antibiotics | Use with `--mode similar` / `--mode novel` to bias toward known-like or first-in-class chemotypes. | context-dependent |

#### Safety / toxicity flags

| eos ID | Title | What it predicts | `want_high` |
|---|---|---|---|
| `eos4tcc` | BayeshERG | Probability of hERG channel blockade (IC50 ≤ 10 µM cut-off). | `false` |
| `eos1pu1` | Cardiotoxicity Classifier | Probability a compound is cardiotoxic. Complements hERG. | `false` |
| `eos5gge` | DILI (early prediction) | 10 DILI-related endpoints; threshold for DILI active = 0.16. | `false` |
| `eos21q7` | InterDILI | Probability of drug-induced liver injury. | `false` |
| `eos69p9` | Tox21 panel | Probability of toxicity across the 12 Tox21 tasks. | `false` |
| `eos481p` | ToxCast panel | Probability of activity across 617 toxicity-relevant biological targets. | `false` |
| `eos6fza` | Toxicity at clinical-trial stage | FDA-approval and clinical-tox probability. Clintox-style. | `false` (for tox) |
| `eos77w8` | Adverse Drug Reactions | Predicted ADRs across 27 groups. | `false` |

### Live lookup (fallback / extension)

When the curated set does not cover the gap — e.g., a pathogen outside the list above, or a more specialised ADMET endpoint — query the Ersilia Model Hub catalogue directly.

**Source**: Airtable base `appR6ZwgLgG8RTdoU`, table `Models` (`tblAfOWRbA7bI1VTB`). Public shared view: <https://airtable.com/appR6ZwgLgG8RTdoU/shr7scXQV3UYqnM6Q/tblAfOWRbA7bI1VTB>.

**Preferred path — Airtable MCP** (only if the user's session has the Airtable MCP available):

1. `mcp__claude_ai_Airtable__list_tables_for_base` with `baseId = "appR6ZwgLgG8RTdoU"` to confirm the `Models` table schema.
2. `mcp__claude_ai_Airtable__list_records_for_table` with:
   - `baseId = "appR6ZwgLgG8RTdoU"`, `tableId = "tblAfOWRbA7bI1VTB"`,
   - `fieldIds = ["Identifier", "Title", "Interpretation", "Subtask", "Biomedical Area", "Target Organism", "Tag", "Status"]`,
   - filter on `Status = "Ready"` (singleSelect — use `get_table_schema` first to resolve the choice ID),
   - and a `contains` filter on `Title`, `Tag`, `Biomedical Area`, or `Target Organism` matching the gap (e.g. `"Schistosoma"`, `"cytochrome"`, `"solubility"`).
3. The table has ~170 Ready models — page through with `cursor` if needed.

**Fallback — WebFetch**: GET the shared view URL above and parse the rendered HTML for model rows. Less reliable than the MCP path; only use when the MCP is unavailable.

For any model found via live lookup, immediately fetch its per-model metadata using `ersilia-metadata-guide.md` to confirm `Title`, `Interpretation`, `Task`/`Subtask`, and the `run_columns.csv` schema before recommending it.

### How to write a recommendation

For each recommended model, the report must state, in this order:

1. **eos ID** as a code span, linked to `https://github.com/ersilia-os/{model_id}`.
2. **What it predicts** — one sentence, drawn from the model's `Interpretation` (preferred) or `Title`.
3. **Why it fits this dataset** — one sentence tying it to a specific gap (e.g. "the dataset has no safety columns and the top candidates include known hERG-prone scaffolds", or "the screen targets *M. tuberculosis* but no TB-specific activity column is present").
4. **Caveats** — one short clause if relevant (e.g. organism trained only on *E. coli*; output is inverted; CNS-only relevance).

Limit recommendations to **1–3 per category** to keep the report actionable. Prefer breadth (one ADMET + one antimicrobial + one safety) over depth in a single area.

---

## Output contract — new audit report sections

The `molecule-auditing` SKILL.md report template adds two sections that draw on this guide. They live alongside the existing report structure; they do not replace anything.

### `## Ersilia columns used`

A table covering every Ersilia output column detected in the dataset, in this order:

| Column | eos ID | Bucket | Role in this audit |
|---|---|---|---|
| `inhibition_50um.eos4e40` | `eos4e40` | `filterable_quantitative` | Primary efficacy — drives ranking |
| `ames.eos7m30` | `eos7m30` | `filterable_flag` | Safety flag — drops molecules with prob > 0.5 |
| `embedding_*.eos…` | `eos…` | `informational` | Not used for filtering; available for clustering |
| `logp.eos7m30` | `eos7m30` | `range_constrained` | Lipinski filter (≤ 5) |
| `…` (unfetchable) | `eos…` | `ambiguous` | Listed in Caveats; not used for filtering |

This section sits **before** the existing "Audit Results" → "Top Candidates" section so the reader sees what drove the ranking before seeing the ranking.

### `## Recommended additional Ersilia models`

A flat bulleted list, grouped by the three categories. Skip any category fully covered by columns already in the dataset. If a category is fully covered, say so explicitly in a one-line note rather than omitting the heading silently.

```markdown
### ADMET / physicochemical
- [`eos2lqb`](https://github.com/ersilia-os/eos2lqb) — Probability of high human oral bioavailability. The dataset has activity and safety coverage but no absorption signal; this would help prioritise orally-deliverable hits.

### Antimicrobial activity
- _Already covered_ — `eos9ivc` (antituberculosis activity) is present.

### Safety / toxicity
- [`eos4tcc`](https://github.com/ersilia-os/eos4tcc) — Probability of hERG channel blockade. None of the existing columns flag cardiac liability; recommended as a hard safety gate before progressing any hit.
- [`eos5gge`](https://github.com/ersilia-os/eos5gge) — Drug-Induced Liver Injury prediction. Complements hERG for a minimum safety triage.
```

This section sits **at the end** of the Audit Results, just before Caveats — it points forward, not at the current screen.
