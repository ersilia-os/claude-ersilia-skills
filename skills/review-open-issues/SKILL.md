---
description: Review and summarize all open issues in the Ersilia CLI repository (ersilia-os/ersilia)
argument-hint: [--label <label>] [--limit <n>]
allowed-tools: [Bash, AskUserQuestion]
---

# Review Open Issues in the Ersilia CLI Repository

You are reviewing all open issues in the [ersilia-os/ersilia](https://github.com/ersilia-os/ersilia) GitHub repository and producing a concise summary.

## Parse Arguments

- `--label <label>` (optional): Filter issues by a specific label (e.g. `bug`, `enhancement`)
- `--limit <n>` (optional): Maximum number of issues to fetch. Default: 200

## Step 1: Fetch Open Issues

Use the `gh` CLI to fetch open issues:

```bash
gh issue list --repo ersilia-os/ersilia --state open --limit <limit> --json number,title,labels,assignees,createdAt,updatedAt,body,milestone,comments
```

If `--label` was provided, add `--label <label>` to the command.

## Step 2: Analyze and Group

Group issues into the following categories based on their labels and titles. An issue can belong to more than one category if it has multiple relevant labels:

- **Bugs** — labeled `bug` or title contains "error", "fail", "crash", "broken", "fix"
- **Enhancements / Feature Requests** — labeled `enhancement`, `feature`, or `feature request`
- **Documentation** — labeled `documentation`, `docs`
- **Good First Issues** — labeled `good first issue`
- **Help Wanted** — labeled `help wanted`
- **Model-related** — labeled `model`, or title/body references a specific model ID (eosXXXX pattern)
- **Stale / Inactive** — open for more than 90 days with no recent update (updatedAt older than 90 days ago)
- **Uncategorized** — issues that do not match any of the above

## Step 3: Present Summary

Present a structured summary in this format:

---

## Ersilia CLI — Open Issues Summary

**Total open issues**: N
**Fetched**: N (of up to <limit>)
**As of**: <today's date>

### By Category

| Category | Count |
|----------|-------|
| Bugs | N |
| Enhancements / Feature Requests | N |
| Documentation | N |
| Good First Issues | N |
| Help Wanted | N |
| Model-related | N |
| Stale / Inactive (>90 days) | N |
| Uncategorized | N |

### Bugs (N)
For each bug issue, one line:
- **#<number>** [<title>](<github-url>) — <one-sentence description from title/body> _(opened <relative date>)_

### Enhancements / Feature Requests (N)
Same one-line format.

### Model-related (N)
Same one-line format.

### Good First Issues (N)
Same one-line format — these are highlighted as good entry points for new contributors.

### Help Wanted (N)
Same one-line format.

### Documentation (N)
Same one-line format.

### Stale / Inactive (N)
Same one-line format, noting how long since last update.

### Uncategorized (N)
Same one-line format.

---

### Top 5 Oldest Open Issues
List the 5 issues with the earliest `createdAt`, regardless of category:
- **#<number>** [<title>](<github-url>) — open since <date>

### Recently Opened (last 7 days)
List issues opened in the last 7 days:
- **#<number>** [<title>](<github-url>) — opened <relative date>

---

Keep descriptions brief. Do not reproduce full issue bodies. The goal is a quick orientation, not exhaustive detail.
