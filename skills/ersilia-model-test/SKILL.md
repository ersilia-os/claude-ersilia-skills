---
name: ersilia-model-test
description: Tests and debugs an Ersilia Model Hub model before hub incorporation. Runs `ersilia test --shallow` on a locally cloned model repository, identifies failing checks, diagnoses and fixes issues in the model code, explains what was wrong and what was fixed to the user, then re-runs the test. Loops until all non-trivial checks pass. Use this skill whenever a user wants to test, validate, or debug an Ersilia model before submitting it to the hub, mentions test failures, says "the test is failing", or is preparing a model for hub incorporation. Trigger even if the user just says "test the model" or "run ersilia test" in any Ersilia context.
---

# Ersilia Model Tester and Debugger

Your job is to run the Ersilia shallow test on a locally cloned model, identify and fix any failures, explain what you did, and re-run until the model passes. Do this automatically — don't wait for the user to ask you to fix things.

## What you receive

- The **model ID** (format: `eos` + 4 alphanumeric characters, e.g. `eos4ywv`)
- The **local path** to the cloned GitHub repository (e.g. `/home/user/eos4ywv`)

If either is missing, ask the user before proceeding.

## Step 1: Run the shallow test

Always run the test inside the `ersilia` conda environment. Navigate to the model directory first so the JSON report lands there:

```bash
cd <model_path>
conda run -n ersilia ersilia test <model_id> --shallow --from_dir <model_path>
```

This produces a JSON report `<model_id>-test.json` in the current directory and prints a PASSED/FAILED table to the terminal. Capture both.

**If the test exits early** (the simple run failed), that's the highest-priority failure — fix it first before re-running. Early exit means subsequent checks couldn't run at all.

## Step 2: Read and triage the results

Read `<model_id>-test.json`. It contains boolean results for each check.

**Ignore (not critical for pre-incorporation models):**
- Any check that reports "not present" — these are fields auto-populated after merge (S3 URL, DockerHub URL, model size, incorporation date, etc.)
- Missing contributor and incorporation metadata

**Fix everything else that is FAILED.** Common failure categories and what to do about each are in `references/troubleshooting.md`.

If all non-trivial checks pass, tell the user the model is ready and summarize what you found. You're done.

## Step 3: Diagnose and fix failures

For each FAILED check:

1. **Read the relevant files** before changing anything. Understand what the file is doing and why it might be failing.
2. **Fix the problem** in the model code.
3. **Explain clearly** to the user: what failed, why, and what you changed.

### What you may touch

| File | OK to modify |
|------|-------------|
| `model/framework/code/main.py` (and other Python files in `code/`) | Yes |
| `model/framework/columns/run_columns.csv` | Yes |
| `model/framework/examples/run_input.csv` | Yes |
| `install.yml` | Yes |
| `metadata.yml` | Yes (only the fields that are failing) |
| `model/framework/examples/run_output.csv` | **No** — this file defines the expected output used for consistency checks. Changing it would mask real problems rather than fix them. Only modify it if the user explicitly asks you to. |
| `model/framework/run.sh` | **Never** — do not touch this file under any circumstances. |

If a problem appears to require changes to `run.sh`, look for an alternative fix — the issue is almost always in `main.py`, `install.yml`, or how inputs/outputs are handled.

### Model template structure (for reference)

```
<model_id>/
├── model/
│   ├── framework/
│   │   ├── run.sh              ← NEVER modify
│   │   ├── code/
│   │   │   └── main.py         ← primary model logic
│   │   ├── examples/
│   │   │   ├── run_input.csv   ← 3 example SMILES
│   │   │   └── run_output.csv  ← expected output (do not modify)
│   │   └── columns/
│   │       └── run_columns.csv ← output column metadata
│   └── checkpoints/            ← model weights (don't modify)
├── metadata.yml
└── install.yml
```

See `references/troubleshooting.md` for specific failure types and how to fix them.

## Step 4: Re-run and repeat

After applying fixes, run the test again from scratch:

```bash
cd <model_path>
conda run -n ersilia ersilia test <model_id> --shallow --from_dir <model_path>
```

Repeat the triage-fix-rerun loop until all non-trivial checks pass. If after 3 iterations the same check keeps failing and you're not sure why, stop and describe the failure in detail to the user — include the exact error message and what you've already tried.

## How to explain fixes to the user

After each fix cycle, give a brief, clear summary:
- What check failed
- What the root cause was (one sentence)
- What you changed and in which file

Keep it readable for someone who knows the model but may not know the internals of the testing framework.
