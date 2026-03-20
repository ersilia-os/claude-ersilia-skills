---
description: Take structured meeting minutes dynamically, aware of the agenda and action items
argument-hint: [--agenda <path>] [--attendees <names>] [--output <path>]
allowed-tools: [Read, Write, AskUserQuestion]
---

# Meeting Minutes

You take structured meeting minutes, tracking discussion points, decisions, and action items in real time or from notes.

## Parse Arguments

- `--agenda <path>` (optional): Path to the meeting agenda file
- `--attendees <names>` (optional): Comma-separated list of attendees
- `--output <path>` (optional): Where to save the minutes. Default: current directory

## Step 1: Load Agenda

Read the agenda file if provided. Structure the minutes template around the agenda items.

## Step 2: Record Minutes

For each agenda item, record:
- Summary of discussion
- Decisions made
- Open questions

## Step 3: Capture Action Items

For each action item, record:
- What needs to be done
- Who is responsible
- Due date (if mentioned)

## Step 4: Output

Write the minutes in a clean, shareable format:

---
**Meeting**: [title]
**Date**: [date]
**Attendees**: [names]

### Agenda Item 1: [title]
...

### Action Items
| # | Action | Owner | Due |
|---|--------|-------|-----|
...
