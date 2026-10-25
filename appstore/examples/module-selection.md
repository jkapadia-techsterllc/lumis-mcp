# Example: Module Selection Decision Tree

A solution architect needs to determine which cloud platform modules to implement for a biotech company that currently uses a mix of legacy CRM features and manual processes.

---

## Conversation Flow

**User:**
> We're a biotech company with 500 reps. We use our legacy CRM for sample tracking and call reporting, but events are managed in spreadsheets and email marketing is done through a separate tool. We want to consolidate everything onto the cloud platform. What modules should we implement?

**Assistant** *(calls `traverse_decision_tree` with tree_name="module-selection")*:

> Based on your profile, here's the recommended module selection:
>
> **Tier 1 — Implement Immediately:**
> - **Sample Management** — You're already using this in your legacy CRM. Direct migration path with 92% feature coverage. Priority: consolidate your existing sample compliance workflows.
> - **Call Reporting / Visit Management** — Core CRM functionality. This is your reps' daily workflow — migrate first to minimize disruption.
>
> **Tier 2 — Implement in Phase 2:**
> - **Events Management** — You're currently in spreadsheets, which means no audit trail and no compliance reporting. Moving to the platform gives you speaker management, budget tracking, and regulatory compliance out of the box.
> - **Approved Messaging** — Replacing your separate email tool. Benefits: pre-approved template enforcement, engagement tracking, and integration with call reporting for a unified rep activity view.
>
> **Tier 3 — Evaluate After Go-Live:**
> - **CLM (Content Management)** — Not in your current stack. Consider adding once reps are stable on the new platform. Benefit: compliant detailing with analytics.
> - **Consent Management** — Required if you operate in GDPR/APPI regions. If US-only today, plan for it when you expand internationally.

**User:**
> Why not implement events and email at the same time as the core modules?

**Assistant** *(calls `search_knowledge` with query="phased migration risk reduction")*:

> Phased rollout is recommended for three reasons:
>
> 1. **Change management capacity** — 500 reps absorbing sample management + call reporting changes is already a significant training load. Adding events and email simultaneously increases the failure-to-adopt risk.
>
> 2. **Data migration sequencing** — Sample and call data have referential integrity dependencies (a call references a sample drop). Events and email are independent data streams. Migrating the dependent data first lets you validate the core data model before layering on independent modules.
>
> 3. **Validation complexity** — Each module has its own validation rules. Running all four simultaneously means debugging validation failures across four domains at once. Sequential rollout isolates issues to one domain at a time.

**User:**
> Makes sense. What's the mapping for our legacy sample tracking to the cloud platform?

**Assistant** *(calls `get_module_mapping` with source_module="Samples")*:

> **Legacy Sample Tracking → Cloud Sample Management**
>
> | Legacy Feature | Cloud Equivalent | Coverage | Notes |
> |---------------|-----------------|----------|-------|
> | Sample inventory | Sample Inventory Management | Full | Direct mapping |
> | Sample transactions | Sample Transaction Records | Full | Transaction types map 1:1 |
> | Lot tracking | Lot Management | Partial | Lot-level expiry requires custom config |
> | Sample limits | Sample Limit Engine | Full | Per-product, per-rep, per-period limits |
> | Sample receipts | Electronic Signature Capture | Full | Built-in signature pad |
> | Compliance reporting | Sample Compliance Reports | Full | FDA-ready out of the box |
> | Cold chain tracking | — | Gap | Requires custom development or third-party integration |
>
> **Key gap:** Cold chain tracking (temperature monitoring during sample transport) is not available natively. If this is critical for your biotech products, plan for a custom integration with your cold chain monitoring provider.

---

## Tools Used

1. `traverse_decision_tree` — Module selection based on company profile
2. `search_knowledge` — Phased migration rationale
3. `get_module_mapping` — Detailed feature mapping for sample management
