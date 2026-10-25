# Lumis — Example Prompts

Prompts to try after connecting Lumis. Organized by role — pick what matches your work.

---

## SI / Implementation Consultant

**Migration planning**
- "Assess migration readiness for a pharma company using CLM, Samples, Events, and Approved Email across 8 countries with 3,000 field reps."
- "Walk me through the module selection decision tree — we need closed-loop marketing, sample management, and event management."
- "What's a realistic go-live timeline for a global pharma deploying to EMEA first, then US 6 months later?"
- "We're migrating mid-year. What are the risks of split-year transparency reporting for Sunshine Act compliance?"

**Veeva-to-cloud module mapping**
- "Map all Veeva CLM objects to their cloud equivalents — include field-level mapping and flag any gaps."
- "How does Veeva EM_Event_vod__c map to the target platform? Include the full field mapping for events, attendees, speakers, and budget."
- "Compare Veeva Approved Email field mappings to the target platform's email template model. What tokens have no equivalent?"
- "Map Veeva sample management objects — Sample_Transaction_vod__c, Sample_Lot_vod__c, and Sample_Inventory_vod__c — to the target platform."

**Functional gap analysis**
- "What are the top 5 functional gaps when migrating Veeva Events Management? Rank by compliance risk."
- "Veeva has speaker cap enforcement and nomination workflows. Does the target platform support this natively or do we build custom?"
- "We use Veeva's Event Rule engine heavily. How many rules can we replicate with validation rules vs. custom Apex?"
- "What Veeva CLM features — like key message tracking and CRM-embedded video — have no native equivalent?"

**Configuration & go-live**
- "What does a typical homepage configuration look like for a large pharma with separate sales and medical personas?"
- "Walk me through the go-live readiness checklist for a 2,000-user deployment."
- "What's the recommended release enablement process? Our customer expects setup docs 3 days before sandbox push."
- "How do I set up content restriction mode so reps only see presentations targeted for the account they're visiting?"

---

## Solution Architect / Technical Lead

**Integration design**
- "What integration pattern should we use for MDM data feeds from IQVIA OneKey — batch ETL or event-driven?"
- "Design the middleware architecture for a deployment using MuleSoft with API-led connectivity for CRM, SAP, and MDM."
- "How should we integrate adverse event reporting so field reps can capture safety data that feeds into our pharmacovigilance system?"
- "What's the recommended territory alignment integration pattern for quarterly realignment loads?"
- "How do we synchronize consent preferences across field CRM and digital marketing channels for GDPR/CCPA compliance?"

**Offline sync & mobile**
- "How does the sync engine prevent duplicate record creation during background sync?"
- "What's the difference between delta sync and full sync, and when does the system fall back?"
- "Explain the offline unique identifier mechanism — when can two devices create conflicting records?"
- "Mobile sync is taking over 30 minutes for initial download with 50,000 accounts. What are the benchmarks and tuning options?"

**Performance at scale**
- "We have 15,000 users across 30 countries. What governor limit concerns should we plan for?"
- "What batch job scheduling patterns avoid overlapping execution windows for large data volumes?"
- "What are the top performance anti-patterns in life sciences CRM deployments?"
- "How should we size the territory hierarchy for a deployment with 6 levels and 50,000 account assignments?"

**Data migration**
- "What are the common data migration validation failures and how do I pre-screen for them?"
- "What's the recommended approach for migrating historical sample transaction data while maintaining PDMA audit trails?"
- "How do I validate that consent records migrated correctly — what are the key fields to verify?"

---

## Pharma IT / CRM Admin

**Day-to-day operations**
- "Our field reps report that presentations shown during a visit don't match the account's targeted content. What should I check?"
- "Territory email template assignments aren't being created automatically. Is this a known issue?"
- "After the latest release, some layouts aren't rendering correctly on iPad. What's the metadata cache invalidation checklist?"
- "How should I classify a reported issue — bug, configuration problem, or working as designed? What's the triage framework?"

**Release & upgrade management**
- "What's the monthly release cadence and how do I prepare the sandbox for a major version upgrade?"
- "What are the rollback criteria and procedures if a release causes issues in production?"
- "Our custom Apex triggers broke after an upgrade. What are the compatibility checkpoints I should have run?"
- "How do I validate that a patch release is safe to apply vs. waiting for the next monthly?"

**Troubleshooting**
- "Users see '--None--' on a required picklist field on iPad but not on web. Is this a known platform difference?"
- "'Send unless recipient opted out' is cancelling emails for HCPs with no consent record at all. What's happening?"
- "Sample transactions are creating duplicates when reps work offline and then sync. How do I fix this?"
- "Visibility rules on newly created records hide field sections until the first sync. Is this expected?"

---

## Regulatory / Compliance Lead

**21 CFR Part 11 (US FDA)**
- "What does 21 CFR Part 11 require for electronic signatures in our sample management workflows?"
- "Walk me through the audit trail requirements under 11.10(e) — what must the CRM log for every record change?"
- "We need GxP validation for our CRM. Explain the IQ/OQ/PQ protocol and where a configured cloud platform falls in GAMP 5."
- "What revalidation is required when switching CRM platforms mid-study? How do we maintain chain of custody for sample data?"
- "How do we ensure ongoing Part 11 compliance when the platform pushes monthly releases?"

**EU sample regulations**
- "Compare EU sample limits across all 20+ countries — which are the strictest?"
- "What's Germany's annual sample limit per HCP and how does it differ from France?"
- "How do Nordic countries handle pharmaceutical sample distribution rules differently?"
- "A field rep covers both Belgium and the Netherlands. How do cross-border sample rules apply?"
- "Which EU countries have outright bans on pharmaceutical samples vs. annual quantity limits?"

**US state-by-state requirements**
- "Which US states require additional licensing beyond federal PDMA for sample distribution?"
- "California requires a furnishing number for NPs and PAs to receive samples. How should the CRM validate this?"
- "What's the difference between New York's CSR requirements and Texas's site-based prescriptive authority?"
- "Our reps distribute controlled substances. What DEA registration validation do we need in the CRM?"
- "How do I configure license expiration alerts with 90/60/30-day thresholds for state-specific requirements?"

**GDPR, APPI & consent**
- "What GDPR constraints apply to HCP consent management in the CRM? How granular must opt-in/opt-out be?"
- "How does Japan's APPI differ from EU GDPR for pharmaceutical data handling?"
- "What's the right consent data model for a global deployment that spans US, EU, and Japan?"

---

## Quick Demos (30 seconds each)

Fast prompts to show Lumis's breadth:

1. **Country lookup:** "What are Norway's pharmaceutical sample distribution rules?"
2. **Gotcha surface:** "What are the top gotchas when migrating sample management from Veeva?"
3. **Terminology:** "What's the correct modern platform term for 'Veeva CRM Online'?"
4. **Decision tree:** "Start the migration path decision tree."
5. **Diagnosis:** "Diagnose: sample transactions are duplicating during offline sync."
6. **Readiness score:** "Assess migration readiness: 4 modules, 3 countries, 500 users."
7. **Regulation:** "What does 21 CFR Part 11 require for e-signatures?"
8. **Field mapping:** "Show me the complete field-level mapping for Veeva EM_Attendee_vod__c."

---

*Every prompt maps to real entries in Lumis's 880+ curated knowledge base. Responses are grounded in life sciences CRM domain expertise — not general-purpose LLM knowledge.*
