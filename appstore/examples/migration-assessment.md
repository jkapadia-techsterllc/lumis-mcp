# Example: Migration Readiness Assessment

A pharmaceutical company is evaluating a move from their legacy CRM to a modern cloud platform. They want to understand the complexity, timeline, and risks before committing.

---

## Conversation Flow

**User:**
> We're a mid-size pharma company running our legacy CRM with CLM, Samples, Events, and Approved Email. We operate in 6 countries (US, Germany, France, Japan, UK, Brazil) with about 2,000 field reps. Can you assess our migration readiness?

**Assistant** *(calls `assess_migration_readiness`)*:

> Here's your migration readiness assessment:
>
> **Complexity Score: 7.2 / 10** (High)
>
> **Module Mapping:**
> | Legacy Module | Cloud Equivalent | Coverage | Gaps |
> |--------------|-----------------|----------|------|
> | CLM | Content Management | 85% | Custom slide-level analytics, offline content sync for large media |
> | Samples | Sample Management | 92% | Lot-level expiry tracking requires custom configuration |
> | Events | Events Management | 78% | Speaker management and budget tracking need custom development |
> | Approved Email | Approved Messaging | 88% | Template migration requires manual mapping of merge fields |
>
> **Key Risks:**
> 1. Japan APPI compliance requires specific consent capture configurations not in the default setup
> 2. Brazil has unique sample distribution regulations that need custom validation rules
> 3. 6-country deployment means 6 regulatory frameworks to validate simultaneously
>
> **Estimated Timeline:** 14–18 months for full migration with parallel go-lives
>
> **Recommendation:** Start with a 2-country pilot (US + Germany) covering CLM and Samples. This reduces risk and validates the module mapping before scaling.

**User:**
> What are the biggest gotchas for the CLM migration specifically?

**Assistant** *(calls `get_gotchas` with module="CLM")*:

> Here are the top gotchas for CLM migration:
>
> 1. **Offline content sync size limits** — The cloud platform has a per-device content cache limit. If your CLM presentations exceed 2GB per rep, you'll need to implement content segmentation by territory.
>
> 2. **Slide-level analytics mapping** — Legacy CRM tracks slide views at the individual slide level. The cloud platform tracks at the presentation level by default. You need to enable enhanced analytics and map the legacy data model.
>
> 3. **Approved content workflow** — The approval chain in the legacy system uses a flat approval list. The cloud platform uses a hierarchical approval process. Migration requires rebuilding the approval workflows, not just moving the data.
>
> 4. **PDF rendering differences** — Content rendered on the legacy platform's built-in viewer may look different in the cloud platform's viewer. Test all CLM content on target devices before go-live.

**User:**
> Good to know. What about the Japan APPI rules you mentioned?

**Assistant** *(calls `get_country_rules` with country="Japan")*:

> Japan's Act on Protection of Personal Information (APPI) requires:
>
> 1. **Explicit opt-in consent** — Unlike GDPR's lawful basis options, APPI requires explicit written or digital consent for every data processing purpose. Configure the consent module for opt-in only.
>
> 2. **Cross-border transfer restrictions** — Personal data transferred outside Japan requires that the destination country has equivalent protections OR individual consent per transfer. This affects your cloud hosting configuration.
>
> 3. **Data retention limits** — APPI mandates deletion when the purpose of use is fulfilled. Configure automated retention policies per data category.
>
> 4. **Breach notification within 3-5 days** — Faster than GDPR's 72 hours in practice because of the business-day counting method. Ensure your incident response process accounts for this.

---

## Tools Used

1. `assess_migration_readiness` — Initial complexity scoring and module mapping
2. `get_gotchas` — Module-specific pitfalls for CLM
3. `get_country_rules` — Japan APPI regulatory requirements
