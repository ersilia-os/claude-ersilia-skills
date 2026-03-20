---
description: Audit small molecules from an Ersilia screening and score them according to drug discovery parameters
argument-hint: <molecules-path> [--context <disease-or-target>] [--output <path>]
allowed-tools: [Read, Bash, Write, WebFetch, AskUserQuestion]
---

# Molecule Auditing

You audit a list of small molecules from an Ersilia screening run and score them according to drug discovery criteria.

## Parse Arguments

- `<molecules-path>` (required): Path to a CSV file with SMILES and associated scores from an Ersilia run
- `--context <disease-or-target>` (optional): The therapeutic context (e.g., "malaria", "M. tuberculosis", "hERG")
- `--output <path>` (optional): Output path for the audit report

## Step 1: Load Molecules

Read the CSV file. Identify the SMILES column and all score columns.

## Step 2: Score Each Molecule

For each molecule, evaluate or retrieve (from the Ersilia model outputs already in the file):
- Predicted activity (from the screening scores)
- Drug-likeness (Lipinski's rule of five, if not already present)
- Predicted ADMET flags (toxicity, solubility, permeability — use available columns)
- Novelty (flag if it matches known drugs or common screening artefacts)
- Pan-assay interference (PAINS) flags

## Step 3: Classify

Classify each molecule as: **Promising** / **Borderline** / **Deprioritise** based on the combined scores.

## Step 4: Output

Produce an audit table with per-molecule scores and classifications, plus a summary of top candidates with a brief justification for each.
