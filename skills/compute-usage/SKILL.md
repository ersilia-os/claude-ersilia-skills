---
description: Track usage and costs of compute resources across Ersilia's network
argument-hint: "[--source <path-or-url>] [--period <YYYY-MM>]"
allowed-tools: [Read, Bash, Write, AskUserQuestion]
---

# Compute Usage Tracking

You summarise usage and estimated costs of compute resources (cloud, HPC, local servers) across Ersilia's network.

## Parse Arguments

- `--source <path-or-url>` (optional): Path to usage logs, billing exports, or a cloud dashboard URL
- `--period <YYYY-MM>` (optional): Month to analyse. Default: current month

## Step 1: Load Usage Data

Read the provided usage logs or billing exports. Check references for any cost baselines or budget allocations.

## Step 2: Summarise Usage

Break down usage by:
- Resource type (CPU, GPU, storage, network)
- Provider (AWS, GCP, Azure, local, HPC cluster)
- Project or model (if attributable)
- User or team member (if available)

## Step 3: Cost Analysis

Estimate or report actual costs. Flag any resources that are:
- Unusually expensive
- Idle or underutilised
- Approaching budget limits

## Step 4: Report

Produce a usage summary table and a short narrative with recommendations for cost optimisation.
