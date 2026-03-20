---
description: Review scientific literature to find AI/ML models and datasets relevant to Ersilia's mission
argument-hint: [--topic <topic>] [--n <number>] [--since <YYYY>]
allowed-tools: [WebSearch, WebFetch, Read, Write, AskUserQuestion]
---

# Model Discovery

You search the scientific literature for machine learning models and datasets that could be incorporated into the Ersilia Model Hub.

## Parse Arguments

- `--topic <topic>` (optional): A specific disease, property, or area of interest (e.g., "malaria", "ADMET", "antimicrobial resistance")
- `--n <number>` (optional): Maximum number of models to return. Default: 20
- `--since <YYYY>` (optional): Only include publications from this year onwards. Default: 3 years ago

## Step 1: Search Literature

Use WebSearch to find recent publications describing predictive models relevant to Ersilia's focus areas (neglected diseases, ADMET, drug discovery for the Global South).

## Step 2: Evaluate Each Model

For each model found, assess:
- Is the source code publicly available (GitHub, Zenodo, etc.)?
- Is the model trained on small molecules (SMILES input)?
- Is the output useful for drug discovery screening?
- Has it already been incorporated into the Hub? (check ersilia-os on GitHub)
- License compatibility

## Step 3: Score and Rank

Rank by: relevance to Ersilia's mission, availability of code, quality of publication, recency.

## Step 4: Report

Produce a ranked table with: model name, publication, code URL, input/output description, relevance score, and a recommended action (incorporate / monitor / skip).
