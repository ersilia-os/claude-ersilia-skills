---
description: Summarise a scientific paper and contextualise it within Ersilia's interests
argument-hint: <pdf-path-or-url>
allowed-tools: [Read, WebFetch, Write, AskUserQuestion]
---

# Paper Summary

You summarise a scientific paper and situate it in the context of Ersilia's mission and model hub.

## Parse Arguments

- `<pdf-path-or-url>` (required): Local path to a PDF or URL of the paper

## Step 1: Read the Paper

Read the full paper (or fetch it if a URL is provided).

## Step 2: Summarise

Produce:
- **TL;DR** (2–3 sentences): what the paper does and why it matters
- **Background**: what problem it addresses
- **Methods**: what approach is used (model type, data, training)
- **Results**: key findings and metrics
- **Limitations**: what the authors acknowledge as gaps
- **Code/data availability**: links if mentioned

## Step 3: Ersilia Context

Answer:
- Is this model/dataset relevant for Ersilia's hub?
- What disease areas or properties does it cover?
- Could it be incorporated as an Ersilia model?
- Does it cite or overlap with existing Ersilia models?

## Step 4: Output

Present the summary in a readable format (500–800 words total).
