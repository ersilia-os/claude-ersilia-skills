---
description: Suggest content topics for Ersilia's social media, blog, and newsletter
argument-hint: [--n <number>] [--channel <social|blog|newsletter|all>] [--theme <theme>]
allowed-tools: [WebSearch, WebFetch, Read, Write, AskUserQuestion]
---

# Topic Suggestion

You suggest relevant content topics for Ersilia's communications channels based on current trends, Ersilia's mission, and the content calendar.

## Parse Arguments

- `--n <number>` (optional): Number of topic suggestions. Default: 10
- `--channel <social|blog|newsletter|all>` (optional): Target channel. Default: all
- `--theme <theme>` (optional): A specific theme or area to focus on

## Step 1: Load Context

Read references for Ersilia's mission, recent posts, and any existing content calendar.

## Step 2: Identify Trends

Use WebSearch to identify current trends in: AI/ML in drug discovery, global health, open science, infectious diseases, Africa/Global South tech.

## Step 3: Generate Suggestions

For each suggested topic, provide:
- Topic title
- Target channel(s)
- Brief description (1–2 sentences)
- Suggested format (post, thread, article, infographic, etc.)
- Why it's relevant now

## Step 4: Output

Present topics in a prioritised list.
