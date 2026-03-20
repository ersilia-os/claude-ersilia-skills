---
description: Monitor Ersilia Model Hub for unused models, stored data, and maintenance needs
argument-hint: "[--threshold-days <n>] [--output <path>]"
allowed-tools: [Bash, WebFetch, Read, Write, AskUserQuestion]
---

# Model Monitoring

You audit the Ersilia Model Hub for models that are unused, have stored data issues, or need maintenance attention.

## Parse Arguments

- `--threshold-days <n>` (optional): Number of days without activity to flag a model as potentially stale. Default: 180
- `--output <path>` (optional): Path to save the report

## Step 1: Fetch Model Inventory

List all models in the Hub using the Ersilia CLI or GitHub API. For each model, gather:
- Model ID and slug
- Last run / last updated date
- Storage usage (if available)
- Status (In progress / Ready / Retired)
- Docker image availability

## Step 2: Flag Issues

Identify models that:
- Have not been run in more than `--threshold-days` days
- Have no Docker image
- Have Status "In progress" older than 6 months
- Have storage data with no recent access
- Have broken or missing source code links

## Step 3: Prioritise

Classify flagged models as: retire / update / investigate.

## Step 4: Report

Produce a monitoring report with a summary table and recommended actions.
