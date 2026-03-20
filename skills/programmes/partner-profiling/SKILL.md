---
description: Profile people and organisations based on Ersilia's parameters of interest
argument-hint: <name-or-url> [--type <person|org>]
allowed-tools: [WebFetch, WebSearch, Read, Write, AskUserQuestion]
---

# Partner Profiling

You generate a structured profile of a person or organisation to assess their relevance and fit for Ersilia partnerships.

## Parse Arguments

- `<name-or-url>` (required): Name of the person/organisation, or a URL (website, LinkedIn, etc.)
- `--type <person|org>` (optional): Whether the subject is a person or an organisation. Infer if not provided.

## Step 1: Gather Information

Use WebSearch and WebFetch to collect publicly available information about the subject.

## Step 2: Build the Profile

### For a person:
- Name, role/title, affiliation
- Research areas or areas of work
- Publications or notable projects
- Geographic location
- Connection to global health / AI / open science
- Previous interactions with Ersilia (if known)

### For an organisation:
- Name, type (NGO, funder, academic, industry, government)
- Mission and focus areas
- Geographic presence
- Funding/grant history (if funder)
- Key contacts (if identifiable)
- Connection to Ersilia's mission

## Step 3: Relevance Assessment

Score the subject across Ersilia's key parameters:
- Mission alignment (1–5)
- Geographic relevance (1–5)
- Collaboration potential (1–5)
- Funding potential (1–5, for funders/orgs only)

## Step 4: Output

Write a concise profile document (300–600 words) with the structured data and a brief narrative summary.
