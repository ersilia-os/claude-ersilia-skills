---
description: Discover relevant events for Ersilia and produce a classified summary report
argument-hint: [--horizon <days>] [--category <science|philanthropy|local|global|all>]
allowed-tools: [WebSearch, WebFetch, Write, AskUserQuestion]
---

# Event Discovery

You search for upcoming events relevant to Ersilia and produce a structured report classifying them by type.

## Parse Arguments

- `--horizon <days>` (optional): How far ahead to look. Default: 90 days
- `--category <science|philanthropy|local|global|all>` (optional): Filter by category. Default: all

## Step 1: Search for Events

Use WebSearch to find relevant upcoming events (conferences, workshops, summits, webinars) in areas such as:
- Infectious disease / global health
- AI/ML in drug discovery
- Open science and open source
- Philanthropy and non-profit tech
- Africa / Global South focused events

## Step 2: Classify Each Event

For each event found, record:
- Name, date, location (or online)
- Organiser
- Category: science / philanthropy / local / global
- Relevance to Ersilia (high / medium / low) with a one-line justification
- Submission deadline (for abstracts/proposals, if applicable)
- URL

## Step 3: Report

Present events sorted by date, grouped by category. Highlight high-relevance events and any approaching deadlines.
