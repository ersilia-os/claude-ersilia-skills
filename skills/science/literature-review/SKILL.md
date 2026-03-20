---
description: Produce a structured literature review on a topic relevant to Ersilia's research interests
argument-hint: <topic> [--n <number>] [--since <YYYY>] [--output <path>]
allowed-tools: [WebSearch, WebFetch, Read, Write, AskUserQuestion]
---

# Literature Review

You conduct a structured literature review on a given topic, contextualised within Ersilia's areas of interest.

## Parse Arguments

- `<topic>` (required): The research topic (e.g., "graph neural networks for antimicrobial resistance")
- `--n <number>` (optional): Number of papers to include. Default: 20
- `--since <YYYY>` (optional): Earliest publication year. Default: 5 years ago
- `--output <path>` (optional): Save the review to this path

## Step 1: Search

Use WebSearch and WebFetch to find relevant papers on the topic. Prioritise peer-reviewed publications and well-cited preprints.

## Step 2: Screen and Select

Select the most relevant papers. Exclude papers that are off-topic or do not contribute new insights.

## Step 3: Synthesise

Organise findings into themes. For each theme, summarise:
- What is known
- Key methods or datasets used
- Gaps or open questions

## Step 4: Contextualise for Ersilia

Highlight findings that are most relevant to: neglected diseases, ADMET, drug discovery for low-resource settings, open-source ML tools.

## Step 5: Output

Produce a structured review with: introduction, thematic sections, summary table of key papers, and a section on implications for Ersilia.
