---
description: Incorporate a published ML model into the Ersilia Model Hub
argument-hint: <repo-url> [--paper <paper-url>] [--model-id <eosXXXX>] [--output-dir <path>]
allowed-tools: [Bash, Read, Write, Edit, Glob, Grep, WebFetch, AskUserQuestion]
---

# Model Incorporation

You incorporate a machine learning model into the Ersilia Model Hub by wrapping it in the eos-template format.

> See `references/eos-template-knowledge.md` for the full knowledge base on eos-template structure, metadata vocabulary, and validation reference compounds.

## Parse Arguments

- `<repo-url>` (required): GitHub or Zenodo URL of the source model
- `--paper <url>` (optional): URL of the associated publication
- `--model-id <eosXXXX>` (optional): Ersilia model identifier. Generated automatically if not provided.
- `--output-dir <path>` (optional): Output directory. Default: current working directory

## Phase 1: Clone and Analyse

Clone the source repository and read all relevant files to understand the model's inference entry point, inputs, outputs, and dependencies.

## Phase 2: Verify by Running

Install the model in an isolated virtual environment and run it on test molecules (aspirin, ibuprofen, caffeine) to confirm the analysis.

## Phase 3: Assign Model ID and Present Analysis

Generate a unique `eosXXXX` identifier (or use one provided) and present the verified analysis for user confirmation.

## Phase 4: Generate Files

Create the full eos-template directory structure with functional `main.py`, `install.yml`, `metadata.yml`, and example files.

## Phase 5: Test and Report

Run inspect, shallow, and deep validation checks and write a `test_report.json` evidence file.
