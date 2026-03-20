---
description: Perform a SWOT analysis of a grant opportunity, prospect, or strategic initiative for Ersilia
argument-hint: <topic> [--context <url-or-file>]
allowed-tools: [WebFetch, WebSearch, Read, Write, AskUserQuestion]
---

# SWOT Analysis

You perform a structured SWOT (Strengths, Weaknesses, Opportunities, Threats) analysis of a given topic in the context of Ersilia's mission and capabilities.

## Parse Arguments

- `<topic>` (required): The subject of the analysis (e.g., a grant name, a partnership, a strategic initiative)
- `--context <url-or-file>` (optional): Additional context document or URL to inform the analysis

## Step 1: Gather Context

Read references and any provided context file or URL. If the topic is a grant or organisation, use WebFetch to retrieve relevant public information.

## Step 2: Analyse

Produce a structured SWOT:

### Strengths
What does Ersilia bring that makes this opportunity a good fit?

### Weaknesses
Where does Ersilia have gaps relevant to this opportunity?

### Opportunities
What could Ersilia gain or unlock from pursuing this?

### Threats
What risks or challenges could arise?

## Step 3: Recommendation

Provide a brief (150–300 word) narrative recommendation: should Ersilia pursue this? What conditions would make it more or less attractive?
