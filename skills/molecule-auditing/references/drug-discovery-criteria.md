# Drug Discovery Criteria

Reference thresholds and code snippets for evaluating small molecules in a drug discovery context.

---

## Lipinski's Rule of Five (Ro5)

Originally proposed to estimate oral bioavailability. A molecule that violates two or more rules is unlikely to be orally bioavailable.

| Property | Threshold | Meaning |
|---|---|---|
| Molecular weight (MW) | ≤ 500 Da | Larger molecules have poor membrane permeability |
| Lipophilicity (LogP) | ≤ 5 | Too lipophilic → poor solubility and toxicity |
| Hydrogen bond donors (HBD) | ≤ 5 | Counts –OH and –NH groups |
| Hydrogen bond acceptors (HBA) | ≤ 10 | Counts N and O atoms |

### RDKit code snippet

```python
from rdkit import Chem
from rdkit.Chem import Descriptors

def lipinski_violations(smiles):
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return None, []
    mw  = Descriptors.MolWt(mol)
    logp = Descriptors.MolLogP(mol)
    hbd = Descriptors.NumHDonors(mol)
    hba = Descriptors.NumHAcceptors(mol)
    violations = []
    if mw  > 500: violations.append(f"MW={mw:.0f}")
    if logp > 5:  violations.append(f"LogP={logp:.1f}")
    if hbd > 5:   violations.append(f"HBD={hbd}")
    if hba > 10:  violations.append(f"HBA={hba}")
    return len(violations), violations
```

---

## Veber's Rules (Oral Bioavailability)

Complement to Lipinski, focused on rotatable bonds and polar surface area.

| Property | Threshold |
|---|---|
| Topological polar surface area (TPSA) | ≤ 140 Å² |
| Rotatable bonds | ≤ 10 |

```python
tpsa = Descriptors.TPSA(mol)
rot_bonds = Descriptors.NumRotatableBonds(mol)
```

---

## CNS Drug Thresholds

For central nervous system targets, molecules must cross the blood–brain barrier. Stricter rules apply:

| Property | Threshold |
|---|---|
| MW | ≤ 450 Da |
| LogP | 1–5 (too hydrophilic is also a problem) |
| TPSA | ≤ 90 Å² |
| HBD | ≤ 3 |

Trigger these stricter thresholds when `--context` contains terms like: `CNS`, `brain`, `BBB`, `neurological`, `Alzheimer`, `Parkinson`, `schizophrenia`, `epilepsy`.

---

## PAINS (Pan-Assay Interference Compounds)

PAINS are structural motifs that tend to produce false positives in biochemical assays through mechanisms like aggregation, fluorescence interference, or redox activity. They are not necessarily toxic — but a PAINS flag means the activity from a screening assay may not be genuine.

### RDKit code snippet

```python
from rdkit.Chem.FilterCatalog import FilterCatalog, FilterCatalogParams

params = FilterCatalogParams()
params.AddCatalog(FilterCatalogParams.FilterCatalogs.PAINS)
catalog = FilterCatalog(params)

def has_pains(smiles):
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return False, []
    entry = catalog.GetFirstMatch(mol)
    if entry:
        return True, [entry.GetDescription()]
    return False, []
```

---

## Common Ersilia ADMET Column Patterns

These are column names (the `{feature}` part before the `.model_id` suffix) that commonly appear in Ersilia ADMET model outputs. For each, the table shows the `direction` from `run_columns.csv` (value-concept relationship) AND the `scoring_role` / `want_high` you should assign in the column metadata JSON.

Always fetch the actual `run_columns.csv` to confirm `direction`. The table here is a guide for common cases.

| Feature name pattern | `direction` | `scoring_role` | `want_high` | What it measures |
|---|---|---|---|---|
| `inhibition_50um` | `high` | `efficacy` | `true` | Probability of inhibiting a target at 50 µM — primary activity signal |
| `bioavailability_ma` | `high` | `beneficial_admet` | `true` | Oral bioavailability probability |
| `hia_hou` | `high` | `beneficial_admet` | `true` | Human intestinal absorption probability |
| `pampa_ncats` | `high` | `beneficial_admet` | `true` | PAMPA membrane permeability |
| `caco2_wang` | `high` | `beneficial_admet` | `true` | Caco-2 permeability (log cm/s) |
| `bbb_martins` | `high` | `beneficial_admet` | `true` | Blood-brain barrier penetration (CNS targets) |
| `solubility_aqsoldb` | `high` | `beneficial_admet` | `true` | Aqueous solubility (log mol/L) |
| `ames` | `high` | `safety_flag` | `false` | Ames mutagenicity probability — high is a red flag |
| `herg` / `activity_80` | `high` | `safety_flag` | `false` | hERG channel blockade (cardiac risk) — flag > 0.5 |
| `dili` | `high` | `safety_flag` | `false` | Drug-induced liver injury probability |
| `clintox` | `high` | `safety_flag` | `false` | Clinical toxicity probability |
| `carcinogens_lagunin` | `high` | `safety_flag` | `false` | Carcinogenicity probability |
| `nr_*` / `sr_*` | `high` | `safety_flag` | `false` | Tox21 nuclear receptor / stress response endpoints |
| `skin_reaction` | `high` | `safety_flag` | `false` | Skin sensitisation probability |
| `pgp_broccatelli` | `high` | `safety_flag` | `false` | P-gp inhibition / efflux risk |
| `cyp*_veith` | `high` | `safety_flag` | `false` | CYP inhibition (drug-drug interaction risk) |
| `clearance_*` | `high` | `beneficial_admet` | `false` | Metabolic clearance — lower is better (more stable) |
| `half_life_obach` | `high` | `beneficial_admet` | `true` | Half-life — longer is generally better |
| `molecular_weight` | `high` | `physicochemical` | `null` | MW — filter via Lipinski (≤500) |
| `logp` / `lipophilicity_*` | varies | `physicochemical` | `null` | LogP — filter via Lipinski (≤5) |
| `tpsa` | `high` | `physicochemical` | `null` | TPSA — filter via Veber (≤140) |
| `hydrogen_bond_*` | `high` | `physicochemical` | `null` | HBD/HBA — Lipinski filters |
| `qed` | `high` | `beneficial_admet` | `true` | Quantitative drug-likeness (0–1, higher = more drug-like) |

> **Key distinction**: `direction` and `want_high` are not the same. `direction=high` for `ames` means higher value = more mutagenicity. `want_high=false` means we don't want mutagenicity. Always reason from the concept, not from `direction` alone.

### Interpretation note for hERG

hERG blockade is a cardiac safety concern regardless of how it is encoded. Flag any molecule with hERG probability > 0.5 as a `safety_flag`. This applies whether the column is `herg`, `activity_80`, or a similarly named variant.

---

## Scoring Summary

Classification uses a `scoring_role`-based approach:

1. **Aggregate activity score**: computed from `scoring_role == "efficacy"` columns only, using `want_high` to normalise. Do NOT mix ADMET/property columns into the activity score.

2. **Safety flags**: raised by `scoring_role == "safety_flag"` columns when value > `flag_threshold` (typically 0.5 for probabilities). Multiple flags → deprioritise.

3. **Lipinski/Veber rules**: applied to `scoring_role == "physicochemical"` columns via RDKit (if available).

| Factor | Weight in classification |
|---|---|
| Activity rank (top 25%/50%) | Primary — required for Promising |
| Lipinski violations (≥ 2) | Disqualifying for Promising; ≥ 3 → Deprioritise |
| Any safety flag > threshold | Major concern → Deprioritise or Borderline |
| PAINS flag | Deprioritise (activity likely artefactual) |
| Invalid SMILES | Exclude from scoring, note in caveats |
| Structural similarity (--mode novel) | Tanimoto ≥ 0.5 to known antibiotic → downgrade Promising to Borderline |
