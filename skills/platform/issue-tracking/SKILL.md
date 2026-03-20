---
description: Track and summarise open issues across Ersilia's GitHub repositories for tech meetings
argument-hint: [--repo <repo>] [--label <label>] [--limit <n>]
allowed-tools: [Bash, Write, AskUserQuestion]
---

# Issue Tracking

You fetch and summarise open GitHub issues across Ersilia's repositories to support technical tracking meetings.

## Parse Arguments

- `--repo <repo>` (optional): Specific repo (e.g., `ersilia-os/ersilia`). Default: all main repos
- `--label <label>` (optional): Filter by label
- `--limit <n>` (optional): Max issues per repo. Default: 100

## Step 1: Fetch Issues

Use `gh issue list` to fetch open issues from the target repositories.

## Step 2: Categorise

Group issues into:
- Bugs
- Enhancements / Feature Requests
- Documentation
- Good First Issues
- Stale (>90 days inactive)
- Model-related

## Step 3: Meeting Summary

Produce a concise summary formatted for a tech tracking meeting:
- Total open issues by repo
- Top 5 most urgent items
- Issues that need a decision
- Good first issues for new contributors
- Stale issues to close or triage

## Step 4: Output

Write a structured markdown report.
