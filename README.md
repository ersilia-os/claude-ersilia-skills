# Claude Code Skills for Ersilia

A curated collection of Claude Code skills to help the Ersilia team work more effectively across programmes, science, visibility, platform, and day-to-day operations.

> **Early-stage repository (v0)**
>
> This is Ersilia's first attempt to build a systematic library of Claude Code skills. The structure and categories are intentional, but most skills are currently **scaffolded** — they define the workflow and accept the right arguments, but have not yet been fully developed, tested, or validated for production use.
>
> Skills are being built incrementally. Each skill will be reviewed and promoted through the maturity stages (`scaffold → draft → ready`) before it is relied upon. Please check the status column in the catalogue below before using a skill in critical workflows.

---

## What are Claude Code skills?

Claude Code skills are reusable workflow definitions stored as `SKILL.md` files. When this repository is installed as a Claude Code plugin, each skill becomes a slash command available in any Claude Code session. Skills encode step-by-step instructions, argument handling, and references to supporting knowledge-base documents — teaching Claude how to perform a specific Ersilia workflow reliably and consistently.

## Why Ersilia is building skills

Ersilia's work spans science, technology, communications, and operations. Much of the team's expertise lives in people's heads or in scattered documents. Skills are a way to encode that institutional knowledge into reusable AI workflows — making expert-level processes accessible to every contributor, reducing onboarding friction, and ensuring consistent quality across the organisation.

---

## Skill Catalogue

| Category | Skill | Description | Status |
|----------|-------|-------------|--------|
| **Programmes** | [grant-tracking](skills/programmes/grant-tracking/) | Track existing grants, discover new opportunities, and highlight key timelines | `scaffold` |
| **Programmes** | [partner-profiling](skills/programmes/partner-profiling/) | Profile people and organisations based on Ersilia's parameters of interest | `scaffold` |
| **Programmes** | [grant-form-filling](skills/programmes/grant-form-filling/) | Fill in a grant application form using Ersilia context documents and the provided form | `scaffold` |
| **Programmes** | [event-discovery](skills/programmes/event-discovery/) | Discover relevant events for Ersilia and produce a classified summary report | `scaffold` |
| **Programmes** | [swot-analysis](skills/programmes/swot-analysis/) | Perform a SWOT analysis of a grant opportunity, prospect, or strategic initiative | `scaffold` |
| **Visibility** | [social-media-post-drafting](skills/visibility/social-media-post-drafting/) | Draft social media posts based on the content schedule and available material | `scaffold` |
| **Visibility** | [newsletter-drafting](skills/visibility/newsletter-drafting/) | Draft Ersilia's monthly newsletter from recent updates, publications, and activities | `scaffold` |
| **Visibility** | [topic-suggestion](skills/visibility/topic-suggestion/) | Suggest content topics for Ersilia's social media, blog, and newsletter | `scaffold` |
| **Visibility** | [impact-tracking](skills/visibility/impact-tracking/) | Summarise Ersilia's impact across social media, website, and model hub metrics | `scaffold` |
| **Visibility** | [branding](skills/visibility/branding/) | Convert documents, slides, or posters into Ersilia-branded formats | `scaffold` |
| **Platform** | [model-incorporation](skills/platform/model-incorporation/) | Incorporate a published ML model into the Ersilia Model Hub | `scaffold` |
| **Platform** | [model-discovery](skills/platform/model-discovery/) | Review scientific literature to find AI/ML models and datasets relevant to Ersilia's mission | `scaffold` |
| **Platform** | [compute-usage](skills/platform/compute-usage/) | Track usage and costs of compute resources across Ersilia's network | `scaffold` |
| **Platform** | [issue-tracking](skills/platform/issue-tracking/) | Track and summarise open issues across Ersilia's GitHub repositories for tech meetings | `scaffold` |
| **Platform** | [model-monitoring](skills/platform/model-monitoring/) | Monitor the Ersilia Model Hub for unused models, stored data, and maintenance needs | `scaffold` |
| **Science** | [literature-review](skills/science/literature-review/) | Produce a structured literature review on a topic relevant to Ersilia's research interests | `scaffold` |
| **Science** | [paper-summary](skills/science/paper-summary/) | Summarise a scientific paper and contextualise it within Ersilia's interests | `scaffold` |
| **Science** | [peer-reviewing](skills/science/peer-reviewing/) | Emulate a peer review of a manuscript and suggest how to address reviewer-style changes | `scaffold` |
| **Science** | [article-formatting](skills/science/article-formatting/) | Reformat a manuscript to match a target journal's figure and section requirements | `scaffold` |
| **Science** | [molecule-auditing](skills/science/molecule-auditing/) | Audit small molecules from an Ersilia screening and score them according to drug discovery parameters | `scaffold` |
| **Day-to-day** | [slack-summaries](skills/day-to-day/slack-summaries/) | Summarise recent Slack activity and surface prioritised action items | `draft` |
| **Day-to-day** | [calendars](skills/day-to-day/calendars/) | Check availability, suggest timeslots, and create calendar events or meeting invites | `scaffold` |
| **Day-to-day** | [time-tracking](skills/day-to-day/time-tracking/) | Analyse how team members have been spending time and assess alignment with objectives | `scaffold` |
| **Day-to-day** | [meeting-minutes](skills/day-to-day/meeting-minutes/) | Take structured meeting minutes dynamically, aware of the agenda and action items | `scaffold` |
| **Day-to-day** | [email-drafting](skills/day-to-day/email-drafting/) | Draft emails on behalf of Ersilia, including pitches, introductions, and follow-ups | `scaffold` |

**Status definitions**:
- `scaffold` — structure and arguments defined; workflow written but not tested or validated
- `draft` — skill has been used and iterated on; mostly reliable but still evolving
- `ready` — skill has been reviewed, tested, and is considered reliable for regular use

---

## Repository Structure

```
claude-ersilia-skills/
├── .claude-plugin/
│   └── plugin.json                     # Plugin manifest
├── skills/
│   ├── programmes/
│   │   ├── grant-tracking/
│   │   │   ├── SKILL.md                # Skill definition
│   │   │   └── references/             # Supporting knowledge-base files
│   │   └── ...
│   ├── visibility/
│   ├── platform/
│   ├── science/
│   └── day-to-day/
└── README.md
```

Each skill follows the same layout: a `SKILL.md` file containing the workflow definition, and a `references/` folder for any supporting documents the skill reads at runtime (e.g., brand guidelines, metadata vocabularies, knowledge bases).

---

## How Skills Are Structured

Every `SKILL.md` file has two parts:

**Frontmatter** — machine-readable metadata:
```markdown
---
description: One-line description of what the skill does
argument-hint: <required-arg> [--optional <value>]
allowed-tools: [Read, Write, WebFetch, Bash, ...]
---
```

**Body** — the workflow Claude follows: argument parsing, step-by-step instructions, output format, and any important rules or constraints.

The `references/` folder holds supporting files that the skill reads using the `Read` tool at runtime — for example, a brand guidelines document for the `branding` skill, or a metadata vocabulary for `model-incorporation`.

---

## Installation

Add this plugin to your Claude Code configuration (`~/.claude/settings.json` or the project-level equivalent):

```json
{
  "plugins": ["https://github.com/ersilia-os/claude-ersilia-skills"]
}
```

Once installed, skills are available as slash commands in any Claude Code session. For example:

```
/model-incorporation https://github.com/org/model-repo --paper https://doi.org/...
/literature-review "graph neural networks for antimicrobial resistance" --since 2022
/email-drafting "pitch to a potential funder" --to "Gates Foundation"
```

---

## Contributing a Skill

Skills are added and improved through pull requests. To contribute:

1. Create a folder at `skills/<category>/<skill-name>/`
2. Add a `SKILL.md` with valid frontmatter (`description`, `argument-hint`, `allowed-tools`) and a step-by-step workflow body
3. Add a `references/` subfolder (can be empty initially, with a placeholder `README.md`)
4. Open a pull request — new skills start at `scaffold` status
5. Skills are promoted to `draft` once they have been used and iterated on, and to `ready` once reviewed and validated

Please keep skills focused on a single, well-defined task. If a workflow is too broad, consider splitting it into multiple skills.

---

## About Ersilia

The [Ersilia Open Source Initiative](https://ersilia.io) is a tech non-profit with the mission to equip laboratories, universities, and clinics in the Global South with AI/ML tools for infectious disease research. Ersilia operates according to the principles of open science, decolonized research, and egalitarian access to knowledge.

The [Ersilia Model Hub](https://github.com/ersilia-os/ersilia) is Ersilia's flagship project — a unified platform of pre-trained AI/ML models for infectious and neglected disease research, covering areas such as antibiotic activity prediction, ADMET prediction, molecular representation, and generative chemistry.

---

## License

GPL-3.0. See [LICENSE](LICENSE) for details.
