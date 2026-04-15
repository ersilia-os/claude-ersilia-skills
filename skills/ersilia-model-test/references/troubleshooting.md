# Ersilia Model Troubleshooting Reference

Common failure types encountered in `ersilia test --shallow`, their causes, and how to fix them. Read this file when a specific check is failing and you need guidance.

---

## 1. Model run fails (early exit)

The test exits early when the basic model execution fails. This is the most critical failure — fix it before anything else.

### Symptom
The test aborts after the first run check. Terminal shows something like:
```
Simple run failed. Exiting test early.
```

### Common causes and fixes

**a) Import error in main.py**

The Python script fails to import a module. Check the error traceback.

- **Relative imports**: If `main.py` uses relative paths like `from ..utils import something`, convert to absolute: `from code.utils import something`. The model is called from the framework root, so paths relative to the package hierarchy break.
- **Missing package**: The import succeeds locally but not in the ersilia environment. Add the package to `install.yml`.

**b) File path errors**

`main.py` receives exactly two arguments from `run.sh`. The `run.sh` calls:
```bash
python $1/code/main.py $2 $3
```
where `$1` is the framework directory (used to locate the script), `$2` is the input CSV, and `$3` is the output CSV. Only `$2` and `$3` are passed to Python, so:

```python
import sys, os

input_file = sys.argv[1]   # DATA_FILE ($2)
output_file = sys.argv[2]  # OUTPUT_FILE ($3)

# To find checkpoints, navigate relative to __file__ (the code directory)
root = os.path.dirname(os.path.abspath(__file__))
checkpoint_path = os.path.join(root, "..", "..", "checkpoints", "model.pkl")
```

The framework dir is NOT in `sys.argv`. Using `__file__` to anchor paths is the correct pattern and matches all working Ersilia models.

**c) Wrong input CSV parsing**

The input file has a header `smiles` (lowercase) and one column of SMILES strings. If the script expects a different column name or no header, fix the parsing:

```python
import csv
with open(input_file) as f:
    reader = csv.reader(f)
    next(reader)  # skip header
    smiles_list = [row[0] for row in reader]
```

**d) Java/external tool not available**

Some legacy models use PaDEL-Descriptor (Java). If the test environment doesn't have Java, the run will fail silently or with a subprocess error. Check if `install.yml` includes `openjdk` as a conda dependency:

```yaml
commands:
  - ["conda", "openjdk", "8.0.412", "conda-forge"]
```

---

## 2. Metadata compliance failures

### Symptom
Checks for `metadata` or `metadata_compliance` fail.

### Fixes

- **Wrong field format**: `metadata.yml` fields are case-sensitive. Values like `Local`, `Online`, `Fixed`, `Variable`, `Score`, `Value` must match exactly.
- **List vs string**: Fields like `Deployment` and `Output` must be YAML lists even with one item:
  ```yaml
  Deployment:
    - Local
  Output:
    - Value
  ```
- **Missing required fields**: The test checks for presence of fields like `Task`, `Subtask`, `Output`, `Output Dimension`, `Output Consistency`. If any are blank or placeholder text ("Biomedical Area 1"), fill them in.
- **"not present" fields**: Fields like `S3`, `DockerHub`, `Model Size`, `Incorporation Date` are auto-populated after merge. These showing "not present" is normal — do not try to fill them.

---

## 3. File structure failures

### Symptom
Check named `file_structure` or similar fails.

### Fixes

- **Missing `columns/run_columns.csv`**: Must exist and have the correct format — one row per output column with fields: `key`, `type`, `direction`, `description`.
  - `key`: lowercase, underscore-separated (e.g. `pIC50_mpro`, `feat_00`)
  - `type`: `Float`, `Integer`, or `String`
  - `direction`: `high` (higher is better), `low` (lower is better), or `unknown`
  - `description`: short human-readable label

- **`run_columns.csv` column names don't match `main.py` output**: The column keys in `run_columns.csv` must exactly match the headers written to the output CSV by `main.py`. Sync them.

- **Missing `examples/run_input.csv`**: Must contain exactly 3 valid SMILES strings with a `smiles` header.

- **`install.yml` formatting error**: The YAML must use list-of-lists syntax for commands:
  ```yaml
  python: "3.10"
  commands:
    - ["pip", "rdkit", "2023.3.1"]
    - ["conda", "openjdk", "8.0.412", "conda-forge"]
  ```
  Not `pip install rdkit` as a string — it must be a list `["pip", "package", "version"]`.

---

## 4. Output format / consistency failures

### Symptom
Checks like `output_consistency`, `output_format`, or `run_consistency` fail.

### Causes

The test checks that:
1. Running the model twice on the same input gives the same output (RMSE = 0 for deterministic models)
2. Running via Ersilia CLI gives the same result as running `bash run.sh` directly
3. Output columns match what `run_columns.csv` declares

### Fixes

**a) Stochastic output on a fixed model**

If the model is marked `Output Consistency: Fixed` in `metadata.yml` but produces different results each run, check:
- Whether dropout is active at inference time — disable it for deterministic models
- Whether any random seed is missing — set it at the top of `main.py`
- Whether temporary file names use timestamps or random IDs — fix to use stable names

**b) Output column mismatch**

If `main.py` writes columns `['feat_0', 'feat_1']` but `run_columns.csv` says `['feature_0', 'feature_1']`, the consistency check fails. Make the names match — edit `run_columns.csv` to match what the code actually outputs (not the other way around, unless the code is wrong).

**c) NaN or empty output**

If the model returns NaN or empty rows for any of the 3 example SMILES, the consistency check will fail. Diagnose why those specific molecules fail — they might be edge cases the model can't process. Fix `main.py` to handle them gracefully (e.g., return 0 or a sentinel value, or log and skip).

---

## 5. Dependency / environment failures

### Symptom
Model fails to run with `ModuleNotFoundError`, `ImportError`, or a conda/pip installation error.

### Fixes

**a) Add a missing package to `install.yml`**

```yaml
python: "3.10"
commands:
  - ["pip", "some-package", "1.2.3"]
```

Pin exact versions. Do not use version ranges — reproducibility requires pinned versions.

**b) Python version mismatch**

If a package requires Python 3.9+ but `install.yml` specifies `python: "3.8"`, update the Python version. Check the package's PyPI page for compatibility.

**c) Conda vs pip conflict**

Some packages (e.g. `rdkit`) are better installed via conda than pip. If pip installation fails or causes conflicts:
```yaml
commands:
  - ["conda", "rdkit", "2023.3.1", "conda-forge"]
```

---

## 6. Debugging workflow (advanced)

If the test fails and the error is not obvious from the test output, reproduce the failure manually:

```bash
# Activate the ersilia env
conda activate ersilia

# Run the model directly (mirrors what run.sh does)
cd <model_path>/model/framework
bash run.sh . examples/run_input.csv /tmp/test_output.csv

# Check the output
cat /tmp/test_output.csv
```

This bypasses the Ersilia test harness and shows the raw error from the model code itself. Fix any errors you see, then re-run the full test.

If the direct bash run works but the Ersilia test still fails, the issue is likely in how Ersilia interprets the output (column names, types, or format).
