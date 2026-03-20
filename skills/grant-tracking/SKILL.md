---
description: Track existing grants, discover new opportunities, and highlight key timelines for Ersilia
argument-hint: "[--source <url-or-file>] [--status <active|upcoming|closed>]"
allowed-tools: [WebFetch, WebSearch, Read, Write, AskUserQuestion]
---

# Grant Tracking

You help Ersilia track active grants, discover new funding opportunities, and surface important deadlines.

## Parse Arguments

- `--source <url-or-file>` (optional): A URL or local file with grant data to parse
- `--status <active|upcoming|closed>` (optional): Filter grants by status. Default: all

## Step 1: Load Existing Grant Data

Read the references folder for any existing grant database or tracker file. If none exists, start a fresh list.

## Step 2: Discover New Opportunities

If no source is provided, search for open grant calls relevant to Ersilia's mission (global health, AI/ML, neglected diseases, open science). Use WebSearch and WebFetch to find relevant funders (Wellcome Trust, NIH Fogarty, Gates Foundation, EU Horizon, etc.).

## Step 3: Compile and Classify

For each grant found, record:
- Funder name and programme
- Grant title and ID (if applicable)
- Status (active / upcoming / closed)
- Deadline (absolute date)
- Amount (if known)
- Eligibility notes
- Relevance to Ersilia's mission (high / medium / low)
- URL / source

## Step 4: Highlight Upcoming Deadlines

List all grants with deadlines in the next 90 days, sorted by urgency.

## Step 5: Report

Present a structured markdown table of all grants, followed by a "Deadlines to Watch" section.
