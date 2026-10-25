# Lumis — Life Sciences CRM Migration Intelligence

[![PyPI](https://img.shields.io/pypi/v/lumis-mcp)](https://pypi.org/project/lumis-mcp/)
[![Python](https://img.shields.io/pypi/pyversions/lumis-mcp)](https://pypi.org/project/lumis-mcp/)
[![License](https://img.shields.io/badge/license-Proprietary-blue)](LICENSE)

<!-- mcp-name: io.github.jkapadia-techsterllc/lumis -->

Lumis is an MCP server that delivers expert-level intelligence for life sciences CRM migrations. It equips AI assistants with a curated knowledge base covering module mapping, regulatory compliance, integration architecture, sync troubleshooting, performance guidance, data validation, decision trees, and operational gotchas — so every recommendation is grounded in domain expertise, not guesswork.

## Quick Start

### Claude Desktop (recommended)

```bash
pip install lumis-mcp
```

Add to `claude_desktop_config.json`:

```json
{
  "mcpServers": {
    "lumis": {
      "command": "lumis-mcp"
    }
  }
}
```

Restart Claude Desktop. You'll see the Lumis tools in the tool picker.

### Claude Code CLI

```bash
pip install lumis-mcp
claude mcp add lumis -- lumis-mcp
```

### uvx (no install)

```json
{
  "mcpServers": {
    "lumis": {
      "command": "uvx",
      "args": ["lumis-mcp"]
    }
  }
}
```

### Remote (Claude.ai / OpenAI)

Connect to the hosted API at `https://api.lumis-lifesciences.com/mcp` with your API key in the `X-Api-Key` header. Sign up at [lumis-lifesciences.com](https://lumis-lifesciences.com).

## What You Get

| Tool | What it does | Free? |
|------|-------------|-------|
| `assess_migration_readiness` | Complexity score, module mappings, gaps, risks, timeline | Yes |
| `get_taxonomy` | Browse the value chain taxonomy — phases, areas, categories | Yes |
| `get_terminology` | Map incorrect legacy terms to correct modern platform terms | Yes |
| `search_knowledge` | Full-text search across 950+ curated entries | |
| `get_module_mapping` | Legacy module to cloud equivalent with field-level gaps | |
| `get_gotchas` | Non-obvious pitfalls for a module or country | |
| `traverse_decision_tree` | Interactive decision trees for module selection, migration paths | |
| `get_country_rules` | GDPR, APPI, FDA 21 CFR Part 11, EU sample limits, US state rules | |
| `run_validation` | Diagnose configuration issues from reported symptoms | |
| `get_agent_workflow` | Structured workflows for migration, implementation, audit, ops | |
| `plan_multi_country_rollout` | Wave-based rollout — country clustering, sequencing, timelines | |
| `compare_entities` | Side-by-side: countries, modules, regulatory frameworks | |
| `plan_system_validation` | CSV/CSA validation plan — GAMP, Part 11, Annex 11, deliverables | |

## Example Prompts

Try these after connecting:

- *"Assess migration readiness for a company using CLM, Samples, Events, and Approved Email across 6 countries with 2,000 users."*
- *"What are the top gotchas when migrating sample management?"*
- *"Get the country rules for Germany — GDPR constraints on consent management and sample distribution limits."*
- *"Plan a 35-country rollout for CLM, Samples, and Events including US and Japan."*
- *"What does 21 CFR Part 11 require for electronic signatures in sample management?"*
- *"Compare Germany vs. France — which has stricter sample management requirements?"*

## Knowledge Base

Lumis ships with **950+ curated knowledge entries** spanning the pharma value chain:

- **Module Mapping** — Legacy CRM to cloud platform with field-level gaps
- **Regulatory Compliance** — 21 CFR Part 11, EU GDPR, Japan APPI, EU sample limits, US state HCP rules
- **Sync Engine Architecture** — Offline-first patterns, conflict resolution, delta sync
- **Integration Patterns** — REST API, MDM feeds, SSO/OAuth, ERP, middleware
- **Performance & Scale** — Data volume planning, governor limits, mobile sync benchmarks
- **Multi-Country Rollout** — Country clustering, wave sequencing, anti-patterns
- **Decision Trees** — Module selection, migration path, regulatory compliance
- **Gotchas** — 65+ non-obvious pitfalls and edge cases
- **Validation Rules** — Symptom-based diagnostic rules
- **System Validation (CSV/CSA)** — GAMP 5, Part 11 mapping, risk assessment framework

## Pricing

| Tier | Price | Access |
|------|-------|--------|
| **Free** | $0 | Migration assessment + terminology + taxonomy |
| **Starter** | $49/mo | Full knowledge base — individual consultants |
| **Professional** | $199/mo | Full KB + priority support — implementation teams |
| **Enterprise** | Contact sales | Custom knowledge overlays + SLA |

The free tier requires no API key.

## Architecture

```
lumis-mcp/
├── server.py              # MCP server with 13 tools
├── knowledge/             # 950+ entries across 280+ files
│   ├── _foundation/       # Org strategy, regulatory, terminology, validation
│   ├── _meta/             # Value chain taxonomy
│   ├── commercialization/ # CRM, safety, regulated content, market access
│   └── clinical/          # Clinical development (expanding)
├── agents/                # 4 agent workflow definitions
├── prompts/               # Agent persona system prompts
└── lumis_mcp/             # PyPI package wrapper
```

## Requirements

- Python 3.10+
- `mcp>=1.0,<3.0`
- `pyyaml>=6.0`

## License and Intellectual Property

This software and its knowledge base are **proprietary** and copyright Lumis AI 2024-2026. All rights reserved.

- **Software**: Licensed for use via MCP clients only. See [LICENSE](LICENSE).
- **Knowledge Base**: 950+ curated entries are trade secrets. Extraction, scraping, reproduction, or use for training ML models is prohibited.
- **Third-party notices**: See [NOTICE](NOTICE).

Unauthorized copying or redistribution will be pursued under applicable law.

---

Built by [Lumis AI](https://lumis-lifesciences.com) — migration intelligence for life sciences.
