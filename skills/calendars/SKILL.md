---
description: Check availability, suggest timeslots, and create calendar events or meeting invites for Ersilia
argument-hint: <meeting-description> [--attendees <emails>] [--duration <minutes>] [--room]
allowed-tools: [Bash, Read, Write, AskUserQuestion]
---

# Calendars

You help manage Ersilia's calendar: checking availability, suggesting meeting times, booking rooms, and creating calendar events.

## Parse Arguments

- `<meeting-description>` (required): What the meeting is about
- `--attendees <emails>` (optional): Comma-separated list of attendee emails
- `--duration <minutes>` (optional): Meeting length in minutes. Default: 60
- `--room` (optional flag): If present, suggest a room booking at Norrsken

## Step 1: Check Availability

Use calendar tools or ask the user to provide availability windows for all attendees.

## Step 2: Suggest Timeslots

Propose 3 candidate timeslots that work for all attendees, prioritising working hours across relevant time zones.

## Step 3: Create Event

Once a timeslot is confirmed, create the calendar event with:
- Title, date/time, duration
- Attendees
- Meeting link (if virtual)
- Agenda (drafted from the meeting description)
- Room booking at Norrsken (if `--room` was specified)

## Step 4: Confirm

Report back with the event details and any booking confirmations.
