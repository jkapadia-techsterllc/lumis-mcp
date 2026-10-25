# Lumis — Life Sciences CRM Migration Intelligence

Lumis is an MCP server that delivers expert-level intelligence for life sciences CRM migrations. It equips AI assistants with a curated knowledge base covering module mapping, regulatory compliance, integration architecture, sync troubleshooting, performance guidance, data validation, decision trees, and operational gotchas — so every recommendation is grounded in domain expertise, not guesswork.

## Why Lumis?

Migrating from a legacy life sciences CRM to a modern cloud platform is one of the highest-risk, highest-cost programs a pharma or biotech company undertakes. The typical failure modes — incorrect module mapping, missed country-specific regulations, broken validation rules, sync engine conflicts, integration misfires, and terminology drift — are all preventable with the right knowledge at the right time.

Lumis packages that knowledge into tools an AI assistant can call, turning Claude (or any MCP-compatible client) into a life sciences CRM migration specialist.

## Capabilities

| Tool | What it does |
|------|-------------|
| `search_knowledge` | Full-text search across 950+ curated entries — modules, gotchas, country rules, validation rules, regulatory compliance, integration patterns, and more |
| `get_module_mapping` | Maps a legacy CRM module to its modern cloud equivalent with coverage level, field-level mapping, and gap analysis |
| `get_gotchas` | Surfaces non-obvious pitfalls for a module or country — the things that burn you in month 8 |
| `traverse_decision_tree` | Walks interactive decision trees for module selection, migration path planning, multi-country rollout planning, and regulatory compliance |
| `get_country_rules` | Regulatory and configuration rules by country — GDPR, APPI, FDA 21 CFR Part 11, EU sample limits, US state HCP license rules, and module-specific constraints |
| `run_validation` | Matches a reported symptom against validation rules to diagnose configuration issues |
| `get_terminology` | Prevents hallucination by mapping incorrect legacy terms to correct modern platform terms |
| `get_agent_workflow` | Full workflow with phases and checklists for each specialized agent type |
| `assess_migration_readiness` | **Free** — no API key needed. Computes complexity score, module mappings, gaps, risks, and timeline |
| `plan_multi_country_rollout` | Generates a wave-based rollout plan — country clustering, wave sequencing, execution timelines, and risk warnings for global deployments |
| `compare_entities` | Side-by-side comparison of any two entities — countries, modules, regulatory frameworks, or wave configurations |

## Use Cases

### For Implementation Consultants
- "We're migrating 12 countries from Veeva. Which modules should we prioritize?"
- "What gotchas should we watch for when migrating closed-loop marketing content?"
- "The customer's consent management is broken after migration — what validation rules should I check?"
- "What are Germany's sample distribution limits vs. France's? How do I configure them?"

### For Solution Architects
- "Map all Veeva modules to their cloud equivalents and flag any coverage gaps."
- "What integration pattern should we use for MDM data feeds — batch ETL or event-driven?"
- "We need to support Japan's APPI and EU GDPR. What country-specific configurations are required?"
- "Walk me through the decision tree for selecting a migration path."

### For Operations Teams
- "Users are reporting duplicate sample transactions after background sync. Diagnose the issue."
- "Mobile sync is taking over 30 minutes for initial download. What are the performance benchmarks?"
- "What's the go-live readiness checklist for a 2,000-user deployment?"

### For Multi-Country Rollout Planning
- "We're deploying CLM, Samples, and Events across 35 countries including US and Japan. Plan the rollout."
- "How should we cluster EU countries into sub-waves for a 5-wave global deployment?"
- "Compare Germany vs. France — which has stricter sample management requirements?"
- "What are the anti-patterns to avoid in multi-country wave planning?"

### For Regulatory / Compliance
- "What does 21 CFR Part 11 require for electronic signatures in sample management?"
- "How do EU country-by-country sample limits differ — Norway vs. Netherlands vs. France?"
- "Which US states require additional documentation beyond federal PDMA for HCP sample distribution?"

## Getting Started

### Option 1: Local (Claude Desktop)

1. Clone the repository:
   ```bash
   git clone https://github.com/lumis-ai/lumis-mcp.git
   cd lumis-mcp
   pip3 install -r requirements.txt
   ```

2. Add to your Claude Desktop config (`claude_desktop_config.json`):
   ```json
   {
     "mcpServers": {
       "lumis": {
         "command": "python3",
         "args": ["/absolute/path/to/lumis-mcp/server.py"]
       }
     }
   }
   ```

3. Restart Claude Desktop. You'll see the Lumis tools in the tool picker.

### Option 2: Remote (Claude.ai Custom Connector)

1. Sign up at [lumis-lifesciences.com](https://lumis-lifesciences.com) to get an API key.
2. In Claude.ai, go to **Settings → Custom Connectors → Add**.
3. Enter the endpoint: `https://api.lumis-lifesciences.com/mcp`
4. Add your API key as the `X-Api-Key` header.

### Option 3: Claude Code CLI

```bash
claude mcp add lumis -- python3 /absolute/path/to/lumis-mcp/server.py
```

### Option 4: OpenAI Custom GPT

1. Sign up at [lumis-lifesciences.com](https://lumis-lifesciences.com) to get an API key.
2. In the GPT Builder, add an Action with the Lumis OpenAPI spec.
3. Configure the API key in the authentication settings.

## Example Prompts

Try these after connecting Lumis:

- *"Assess migration readiness for a pharma company using CLM, Samples, Events, and Approved Email across 6 countries with 2,000 users."*
- *"What are the top gotchas when migrating sample management from Veeva?"*
- *"Walk me through the module selection decision tree for a company that needs closed-loop marketing and event management."*
- *"Get the country rules for Germany — we need to know what GDPR constraints apply to consent management and what the sample distribution limits are."*
- *"Our validation rules are failing on sample lot numbers. Diagnose the issue."*
- *"What does 21 CFR Part 11 require for our e-signature implementation?"*
- *"Compare EU sample limits across all 20+ countries — which are the strictest?"*
- *"What integration pattern should we use for real-time HCP data feeds from a master data provider?"*
- *"The sync engine is creating duplicate visit records during background sync. What's the root cause?"*
- *"What are the performance benchmarks for initial mobile sync with 50,000 accounts?"*

## Pricing

| Tier | Price | Rate Limit | Access |
|------|-------|-----------|--------|
| **Free** | $0 | 10 req/min | Migration readiness assessment + terminology lookup |
| **Starter** | $49/mo | 60 req/min | Full knowledge base — individual consultants |
| **Professional** | $199/mo | 300 req/min | Full knowledge base + regulatory compliance — implementation teams |
| **Enterprise** | Contact sales | 1,000 req/min | Custom knowledge overlays + SLA + dedicated support |

The free tier requires no API key — just connect and run `assess_migration_readiness`.

## Knowledge Base

Lumis ships with **950+ curated knowledge entries** covering:

- **Module Mapping** (35+ files): Veeva CLM, Approved Email, Events, Sample Management, visit management, field coaching, consent, territory alignment, content management, and more — with field-level mapping and gap analysis
- **Sync Engine Architecture** (25 entries): Background vs. manual sync, transaction retention, duplicate prevention, offline-first patterns, conflict resolution, delta sync optimization
- **Integration Patterns** (20 entries): REST API, MDM feeds, SSO/OAuth, ERP integration, middleware patterns, event-driven architecture, bulk API, mobile offline sync
- **Performance & Scale Guide** (18 entries): Data volume planning, governor limits, mobile sync benchmarks, territory hierarchy optimization, batch job scheduling, performance anti-patterns
- **Release & Upgrade Guide** (15 entries): Monthly/major/patch cadence, sandbox validation, custom code compatibility, metadata cache invalidation, rollback criteria
- **Go-Live Readiness Checklist** (15 entries): Data migration validation, UAT sign-off, mobile provisioning, hypercare planning, rollback procedures
- **Investigation & Triage Patterns** (30 entries): Bug vs. configuration vs. as-designed classification, customer-reported issue diagnosis, root cause analysis methodology
- **Implementation Patterns** (50+ entries): Homepage configuration, go-live timelines, extensibility model, escalation processes, FDE engagement
- **Multi-Country Rollout Planning** (25+ entries): Country clustering methodology, regional cluster definitions, wave sequencing rules, anti-patterns, 5-wave reference schedule, sizing guide, sprint-based execution templates, and an interactive rollout planner decision tree
- **Decision Trees**: Interactive flows for module selection, migration path planning, multi-country rollout planning, and regulatory compliance
- **Gotchas** (65+ entries): Non-obvious pitfalls, edge cases, iPad/web parity gaps, sync race conditions, and "things that break in month 8"
- **Validation Rules**: Symptom-based diagnostic rules for sample management, consent management, email templates, and more
- **Regulatory Compliance**:
  - **21 CFR Part 11** (18 entries): Electronic signatures, audit trails, system validation, access controls — mapped to CRM implementation requirements
  - **US State HCP License Rules** (20+ entries): State-by-state sample distribution requirements beyond federal PDMA, NP/PA prescribing authority, DEA registration
  - **EU Country Sample Limits** (30 entries): All 20+ EU/EEA countries with specific annual limits, cross-border rep handling, units-vs-packs counting
  - **EU GDPR**, **US Federal (PDMA/FDA)**, **Japan APPI** — baseline regulatory frameworks
- **Terminology**: Guardrails that map incorrect legacy terms to correct modern platform terms

## Agent Workflows

Lumis supports four specialized agent types, each with a structured workflow:

1. **Migration Agent** — Assessment → module mapping → gap analysis → migration plan
2. **Implementation Agent** — Configuration → data migration → integration setup → validation → go-live readiness
3. **Audit Agent** — Compliance check → regulatory review → validation rule verification → CFR Part 11 attestation
4. **Operations Agent** — Issue diagnosis → sync troubleshooting → root cause analysis → resolution guidance

## Architecture

Lumis is a Python MCP server that loads a structured knowledge base from YAML and JSON files. It supports both local (stdio) and remote (HTTP) transports.

```
lumis/
├── server.py              # MCP server with 11 tools
├── knowledge/platform/    # 950+ curated entries across 72 files
│   ├── modules/           # 45+ module mapping and Q&A files
│   ├── decision-trees/    # Interactive decision flows
│   ├── gotchas/           # Non-obvious pitfalls and troubleshooting
│   ├── validation-rules/  # Diagnostic rules (YAML)
│   ├── country-rules/     # US federal, EU GDPR, CFR Part 11, state HCP rules, EU sample limits, Japan APPI
│   └── terminology/       # Term correction guardrails
├── agents/                # Workflow definitions for 4 agent types
├── prompts/               # System prompts for each agent persona
└── aws/                   # CDK deployment stack (Lambda + API Gateway + DynamoDB)
```

## Zero-Inference-Cost Model

Lumis runs on a zero-inference-cost model for the platform operator. The customer's AI subscription (Claude Pro, Team, Enterprise, or OpenAI Plus/Team) pays for the model inference. Lumis pays only for Lambda compute and DynamoDB reads — typically under $0.01 per request.

## Contributing

Lumis is maintained by Lumis AI. To contribute knowledge entries, submit a pull request with new JSON files in the appropriate `knowledge/platform/` subdirectory.

## License

Proprietary. See [LICENSE](../LICENSE) for details.
