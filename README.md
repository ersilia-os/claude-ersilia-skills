# Claude Code Skills for the Ersilia Model Hub

A collection of Claude Code skills to assist contributors in incorporating, testing, and publishing AI/ML models to the [Ersilia Model Hub](https://github.com/ersilia-os/ersilia).

## What is this?

This repository provides skills that can be installed into Claude Code via the plugin system. Each skill teaches Claude how to perform a specific Ersilia workflow — from incorporating new ML models into the Hub, to testing and publishing them.

## Skills

### `incorporate-model`

Incorporates a published ML model into the Ersilia Model Hub by wrapping it in the standardized `eos-template` format.

**Usage**: `/incorporate-model <repo-url> [--paper <paper-url>] [--model-id <eosXXXX>] [--output-dir <path>]`

**What it does**:
1. **Phase 1 — Clone and Analyze**: Clones the source repository, reads all relevant files, identifies the inference entry point, and determines input/output formats.
2. **Phase 2 — Verify by Running**: Installs the model in an isolated virtual environment and runs it on test molecules (aspirin, ibuprofen, caffeine) to confirm the analysis.
3. **Phase 3 — Assign Model ID**: Generates a unique `eosXXXX` identifier (or uses one provided) and presents the verified analysis for user confirmation.
4. **Phase 4 — Generate Files**: Creates the full `eos-template` directory structure with functional `main.py`, `install.yml`, `metadata.yml`, and example files.
5. **Phase 5 — Test and Report**: Runs inspect, shallow, and deep validation checks, generates a `deep_validation.ipynb` notebook, and writes a `test_report.json` evidence file.

**References**: The skill uses `references/eos-template-knowledge.md` as a knowledge base covering the eos-template structure, metadata vocabulary, and deep validation reference compounds.

## Installation

Add this plugin to your Claude Code configuration:

```json
{
  "plugins": ["https://github.com/ersilia-os/claude-ersilia-skills"]
}
```

Or install locally by pointing to the repository directory.

## Repository Structure

```
claude-ersilia-skills/
├── claude-plugin/
│   └── marketplace.json              # Plugin manifest
├── ersilia-skills/
│   └── incorporate-model/
│       ├── SKILL.md                  # Skill definition (5-phase workflow)
│       └── references/
│           └── eos-template-knowledge.md  # eos-template knowledge base
└── README.md
```

## Contributing

Skills for `publish-model` and `test-model` are planned for future additions. Contributions are welcome via pull request.

## About Ersilia

The [Ersilia Open Source Initiative](https://ersilia.io) is a tech non-profit with the mission to equip laboratories, universities, and clinics in the Global South with AI/ML tools for infectious disease research. Ersilia operates according to the principles of open science, decolonized research, and egalitarian access to knowledge.

The [Ersilia Model Hub](https://github.com/ersilia-os/ersilia) is Ersilia's flagship project — a unified platform of pre-trained AI/ML models for infectious and neglected disease research, covering areas such as antibiotic activity prediction, ADMET prediction, molecular representation, and generative chemistry.

## License

GPL-3.0. See [LICENSE](LICENSE) for details.
