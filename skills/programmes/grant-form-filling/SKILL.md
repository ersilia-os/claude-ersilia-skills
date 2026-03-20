---
description: Fill in a grant application form using Ersilia context documents and the provided form
argument-hint: <form-path-or-url> [--docs <path>] [--output <path>]
allowed-tools: [Read, WebFetch, Write, AskUserQuestion]
---

# Grant Form Filling

You help draft responses to grant application forms using Ersilia's background documents and relevant context.

## Parse Arguments

- `<form-path-or-url>` (required): Path to the grant form (PDF, DOCX, or URL)
- `--docs <path>` (optional): Path to a folder with Ersilia context documents (mission, past grants, impact reports)
- `--output <path>` (optional): Where to save the filled draft. Default: current directory

## Step 1: Read the Form

Read the grant form and list all questions/sections that require a response.

## Step 2: Load Ersilia Context

Read documents from the `references/` folder and any provided `--docs` path. Look for: mission statement, team bios, past grant narratives, impact data, model hub description, technical summaries.

## Step 3: Draft Responses

For each question in the form, draft a response using the available context. Flag questions where information is insufficient with `[NEEDS HUMAN INPUT: ...]`.

## Step 4: Review and Output

Present all draft responses clearly labelled by question. Save to `--output` if specified.

## Important Rules

- Never invent figures, statistics, or facts. Use only information from the provided documents or references.
- Flag every gap explicitly rather than filling it with guesses.
- Match the tone and word count requested by the form.
