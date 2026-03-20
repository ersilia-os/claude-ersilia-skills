---
description: Convert documents, slides, or posters into Ersilia-branded formats
argument-hint: <input-path> [--format <slides|poster|report|diagram>] [--output <path>]
allowed-tools: [Read, Write, AskUserQuestion]
---

# Branding

You help adapt Ersilia documents, slides, diagrams, and posters to match Ersilia's visual and editorial brand guidelines.

## Parse Arguments

- `<input-path>` (required): Path to the input document
- `--format <slides|poster|report|diagram>` (optional): Document type. Infer if not provided.
- `--output <path>` (optional): Output path. Default: same directory as input with `-branded` suffix.

## Step 1: Read the Document

Read the input file and understand its structure and content.

## Step 2: Load Brand Guidelines

Read references for Ersilia's brand guidelines (colours, fonts, tone, logo usage).

## Step 3: Apply Branding

Identify elements to adjust:
- Colour palette (replace with Ersilia brand colours)
- Typography recommendations
- Logo placement
- Slide/section structure
- Tone and language consistency

## Step 4: Output

Produce an annotated version of the document with specific, actionable branding instructions, or (for text-based formats) a directly reformatted output.

## Note

For binary formats (PPTX, PDF), produce a written branding guide specific to the document rather than a direct conversion.
