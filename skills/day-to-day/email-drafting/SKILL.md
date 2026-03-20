---
description: Draft emails on behalf of Ersilia, including pitches, introductions, and follow-ups
argument-hint: <purpose> [--to <recipient>] [--context <path-or-url>]
allowed-tools: [Read, WebFetch, Write, AskUserQuestion]
---

# Email Drafting

You draft professional emails on behalf of Ersilia, incorporating the organisation's mission and context.

## Parse Arguments

- `<purpose>` (required): What the email is for (e.g., "pitch to a potential funder", "introduce Ersilia to a new partner", "follow up on a grant application")
- `--to <recipient>` (optional): Name and/or organisation of the recipient
- `--context <path-or-url>` (optional): Additional context (e.g., a grant brief, a meeting recap, a person's profile)

## Step 1: Load Context

Read any provided context file or URL. Read references for Ersilia's mission, key facts, and contact information.

## Step 2: Draft the Email

Write a professional, concise email:
- **Subject line**: clear and specific
- **Opening**: personalised to the recipient where possible
- **Body**: purpose-driven, mission-grounded, no fluff
- **Call to action**: one clear ask or next step
- **Closing**: warm and professional

Keep it under 300 words unless the purpose requires more detail.

## Step 3: Output

Present the email draft with subject line. Flag any fields that need personalisation (marked as `[FILL IN: ...]`).
