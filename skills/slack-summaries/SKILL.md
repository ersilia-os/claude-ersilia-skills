---
description: Summarise your Slack activity, surface unanswered messages, and identify what you need to respond to
argument-hint: [--since <YYYY-MM-DD|Nd|Nw>] [--channels <ch1,ch2>] [--me <slack-username>]
allowed-tools: [mcp__slack__slack_list_channels, mcp__slack__slack_get_channel_history, mcp__slack__slack_search_messages, mcp__slack__slack_get_thread_replies, mcp__slack__slack_get_users, AskUserQuestion]
---

# Slack Summaries

You summarise the user's recent Slack activity, identify what they need to respond to, and provide a digest of what's been happening across their channels.

## Important: MCP Dependency

This skill requires the Slack MCP server to be installed in Claude Code. If any Slack tool call fails with a "tool not found" or connection error, stop immediately and display:

```
The Slack MCP server is not connected. Please follow the setup guide:
  skills/day-to-day/slack-summaries/references/slack-mcp-setup.md

Then re-run: /slack-summaries
```

Do not attempt to proceed without MCP access.

---

## Parse Arguments

- `--since <value>` (optional): How far back to look. Accepts:
  - `YYYY-MM-DD` (absolute date)
  - `Nd` (e.g. `3d` = last 3 days)
  - `Nw` (e.g. `2w` = last 2 weeks)
  - Default: `7d`
- `--channels <ch1,ch2>` (optional): Comma-separated channel names (without `#`). Default: all channels the user is a member of.
- `--me <username>` (optional): The user's Slack display name or username, used to detect mentions and their own messages. If not provided, ask using AskUserQuestion.

## Step 0: Verify Access and Resolve Identity

1. Call `slack_list_channels` to confirm MCP connectivity. If it fails, show the setup message above and stop.

2. If `--me` was not provided, ask:
   > "What is your Slack username or display name? (Used to detect messages mentioning you or threads you need to reply to.)"

3. Compute the `since_ts` Unix timestamp from `--since`:
   - `Nd`: subtract N × 86400 seconds from now
   - `Nw`: subtract N × 604800 seconds from now
   - `YYYY-MM-DD`: convert to Unix timestamp at 00:00 UTC

## Step 1: Resolve Channel List

If `--channels` was provided, resolve those channel names to IDs. Otherwise, fetch the full list using `slack_list_channels` and keep only channels where `is_member: true`. Exclude archived channels.

## Step 2: Part A — Personal Action Items

This section identifies what the user **needs to do**. Work through these signals:

### 2a. Direct Messages

Fetch recent DM and group DM conversations since `since_ts`. For each DM where the last message was sent by someone else (i.e. the user has not replied), flag it as requiring a response.

### 2b. Mentions

Search for messages that @mention the user across all channels since `since_ts` using `slack_search_messages`. For each mention, read the surrounding context and classify:
- **Must respond** — a direct question or explicit request is addressed to the user
- **FYI** — informational mention, no action expected

### 2c. Threads the user is in but hasn't replied to recently

For threads where the user previously participated, fetch replies with `slack_get_thread_replies`. If someone replied after the user's last message in that thread, flag it as **Should acknowledge**.

### 2d. Threads the user started that have new replies

Look through channel history for messages sent by the user (`--me`). For each thread the user started that has new replies since their last activity, flag it as **Should acknowledge**.

---

## Step 3: Part B — Channel Digest

For each channel in the resolved list, fetch message history since `since_ts` using `slack_get_channel_history`.

For each channel, produce:
- A **2–4 sentence summary** of the main topics discussed
- **Decisions or conclusions** reached (if any)
- **Notable links, files, or announcements** shared (if any)
- Approximate **activity level**: low (<10 messages), moderate (10–50), high (>50)

Skip channels with zero messages in the period. For high-volume channels (>100 messages), summarise the most prominent threads rather than every message.

---

## Step 4: Compose and Present Output

Present results in this order and format:

---

```
## Slack Summary — [since date] to [today]

### Your Action Items

**Must Respond** (N)
- [#channel or DM] @sender — "message preview up to 120 chars…" _(X hours/days ago)_
  💬 Suggested framing: [one sentence on how to respond]

**Should Acknowledge** (N)
- [#channel] @sender replied in your thread — "preview…" _(X hours/days ago)_

**FYI** (N)
- [#channel] @sender mentioned you — "preview…" _(X hours/days ago)_

---

### Channel Digest

**#channel-name** · moderate activity
2–4 sentence summary. Decisions: ... Links: ...

**#channel-name** · low activity
2–4 sentence summary.
```

---

## Rules

- Never fabricate or paraphrase messages in a way that changes their meaning. Use exact quotes for message previews.
- Keep message previews to the first 120 characters.
- Omit channels with no activity in the period — don't list them as empty.
- Omit action item categories that have zero items.
- If there are no action items at all, state: "No action items found for this period."
- Do not surface bot messages or automated notifications in action items — only messages from real humans.
