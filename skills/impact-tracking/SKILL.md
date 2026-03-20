---
description: Summarise Ersilia's impact across social media, website, and model hub metrics
argument-hint: "[--period <YYYY-MM>] [--sources <path>]"
allowed-tools: [Read, WebFetch, WebSearch, Write, AskUserQuestion]
---

# Impact Tracking

You compile and summarise Ersilia's reach and impact metrics across digital channels.

## Parse Arguments

- `--period <YYYY-MM>` (optional): Month to summarise. Default: current month
- `--sources <path>` (optional): Folder with exported analytics files (CSV, JSON)

## Step 1: Load Data

Read any analytics exports from `--sources`. Check references for any benchmark or baseline data.

## Step 2: Compile Metrics

Collect data (from files or by prompting the user) for:
- **Social media**: followers, impressions, engagement rate, top posts
- **Website**: sessions, unique visitors, top pages, geographic distribution
- **Model hub**: downloads, model runs, contributors, new models added
- **GitHub**: stars, forks, issues opened/closed, PRs merged

## Step 3: Analyse

Compare to the previous period. Identify top-performing content or models. Flag any notable spikes or drops.

## Step 4: Report

Write a concise impact summary (~300–500 words) with a key metrics table and 3–5 takeaways.
