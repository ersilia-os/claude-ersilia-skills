---
description: Summarise recent Slack activity and surface prioritised action items for the Ersilia team
argument-hint: [--channels <channel1,channel2>] [--since <YYYY-MM-DD>]
allowed-tools: [Bash, Read, Write, AskUserQuestion]
---

# Slack Summaries

You summarise recent activity from Ersilia's Slack workspace and extract prioritised action items.

## Parse Arguments

- `--channels <channel1,channel2>` (optional): Specific channels to summarise. Default: all relevant channels
- `--since <YYYY-MM-DD>` (optional): Start date for messages. Default: last 7 days

## Step 1: Fetch Messages

Use the Slack CLI or API (or ask the user to provide an export) to retrieve recent messages from the specified channels.

## Step 2: Summarise by Channel

For each channel, write a 2–5 sentence summary of the main discussions.

## Step 3: Extract Action Items

Identify messages that imply a task, decision, or follow-up. For each action item:
- What needs to be done
- Who is responsible (if mentioned)
- Urgency (urgent / normal / low)

## Step 4: Output

Present channel summaries followed by a prioritised action item list.
