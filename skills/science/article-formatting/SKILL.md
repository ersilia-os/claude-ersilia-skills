---
description: Reformat a manuscript to match a target journal's figure and section requirements
argument-hint: <document-path> [--journal <journal-name>] [--output <path>]
allowed-tools: [Read, WebFetch, Write, AskUserQuestion]
---

# Article Formatting

You help reformat a scientific article to match a target journal's requirements for figures, section structure, word counts, and reference style.

## Parse Arguments

- `<document-path>` (required): Path to the manuscript file
- `--journal <journal-name>` (optional): Target journal. If provided, fetch its author guidelines.
- `--output <path>` (optional): Output path for the reformatted document

## Step 1: Read the Manuscript

Read the document and identify its current structure.

## Step 2: Load Journal Guidelines

If a journal is specified, use WebFetch to retrieve its author guidelines. Extract:
- Required sections and order
- Word count limits (abstract, main text)
- Figure format and number limits
- Reference style

Also apply Ersilia's figure standards from the references folder.

## Step 3: Identify Gaps and Mismatches

List all formatting issues: missing sections, overlong abstract, non-compliant reference style, figures without legends, etc.

## Step 4: Reformat

Apply the required formatting changes to the text content. For binary formats, produce an annotated checklist of changes needed.

## Step 5: Output

Produce the reformatted document or a detailed change report.
