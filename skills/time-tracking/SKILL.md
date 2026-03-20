---
description: Analyse how Ersilia team members have been spending time and assess alignment with objectives
argument-hint: "[--user <name-or-email>] [--period <YYYY-MM>] [--source <path>]"
allowed-tools: [Read, Write, AskUserQuestion]
---

# Time Tracking

You analyse time logs and calendar data to summarise how time has been spent and assess alignment with Ersilia's objectives.

## Parse Arguments

- `--user <name-or-email>` (optional): Specific team member. Default: the current user
- `--period <YYYY-MM>` (optional): Month to analyse. Default: current month
- `--source <path>` (optional): Path to a time log export (CSV, JSON, or calendar export)

## Step 1: Load Data

Read the time log or calendar export. If no file is provided, ask the user to describe their recent activity.

## Step 2: Categorise Time

Group activities into categories:
- Meetings (internal / external)
- Deep work (coding, writing, analysis)
- Administration
- Events / travel
- Untracked

## Step 3: Assess Alignment

Compare the time distribution to Ersilia's current priorities and objectives (read from references). Flag imbalances (e.g., too much admin, not enough deep work).

## Step 4: Report

Produce a time summary with a category breakdown chart (ASCII or table) and 3–5 observations or suggestions.
