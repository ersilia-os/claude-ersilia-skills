---
description: Emulate a peer review of a manuscript and suggest how to address reviewer-style changes
argument-hint: <pdf-path-or-url> [--journal <journal-name>]
allowed-tools: [Read, WebFetch, Write, AskUserQuestion]
---

# Peer Reviewing

You emulate a constructive peer review of a scientific manuscript, providing structured feedback in the style of a reviewer report.

## Parse Arguments

- `<pdf-path-or-url>` (required): Path to the manuscript PDF or URL
- `--journal <journal-name>` (optional): Target journal (to calibrate scope and style expectations)

## Step 1: Read the Manuscript

Read the full manuscript carefully.

## Step 2: Overall Assessment

Evaluate:
- Significance and novelty of the contribution
- Appropriateness for the target journal
- Clarity and logic of the narrative
- Overall recommendation: Accept / Minor Revision / Major Revision / Reject

## Step 3: Major Comments

List 3–7 major issues that must be addressed (e.g., missing controls, unclear methods, overclaimed conclusions).

## Step 4: Minor Comments

List specific, line-level suggestions (clarity, missing references, figure labels, statistical reporting).

## Step 5: How to Address

For each major comment, suggest a concrete action the authors can take to address it.

## Step 6: Output

Present the review in standard reviewer report format.
