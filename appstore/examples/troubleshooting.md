# Example: Operations Troubleshooting

An operations specialist is diagnosing production issues reported by customers across multiple regions. They use Lumis to identify root causes and get resolution guidance.

---

## Conversation Flow

**User:**
> Multiple reps in our Japan office are reporting that approved email templates are showing incorrect merge field values — the doctor's name is showing up as the account name instead.

**Assistant** *(calls `get_terminology` with term="merge field")*:

> First, a terminology note: In the modern cloud platform, "merge fields" are called "template tokens." The legacy CRM used merge field syntax (`{{Doctor_Name}}`), while the cloud platform uses token syntax (`{!Contact.Name}`). This distinction matters for diagnosis.

*(calls `run_validation` with symptom="approved email merge field showing wrong value account name instead of doctor")*:

> This matches validation rule **AE-VAL-004: Template Token Object Context Mismatch**.
>
> **Root Cause:** During template migration, merge fields referencing the contact (HCP) record were mapped to the account object instead. This is a common migration error because the legacy CRM used a flat `Doctor_Name` field, while the cloud platform requires explicit object paths (`Contact.Name` vs `Account.Name`).
>
> **Diagnosis:**
> 1. Open the affected approved email template
> 2. Inspect each token — look for tokens starting with `Account.` that should start with `Contact.`
> 3. Common mismatches:
>    - `{!Account.Name}` should be `{!Contact.Name}`
>    - `{!Account.Specialty__c}` should be `{!Contact.Specialty__c}`
>    - `{!Account.Credentials__c}` should be `{!Contact.Credential__c}`
>
> **Fix:** Update the template tokens to reference the correct object. After fixing, the template must go through the approval workflow again before reps can use it.

**User:**
> Thanks. Separately, our events team in France says that speaker fee payments are failing with a "regulatory limit exceeded" error.

**Assistant** *(calls `get_country_rules` with country="France" and module="Events")*:

> France has specific regulations on payments to healthcare professionals under the **Loi Bertrand (Sunshine Act)**.
>
> **Regulatory Context:**
> - France requires public disclosure of all transfers of value above €10 to HCPs
> - Speaker fees have an annual cap per HCP that varies by event type
> - The cloud platform enforces these limits if the France country rules are configured
>
> **Likely Cause:** The "regulatory limit exceeded" error means the cumulative speaker fees for this HCP have hit the configured annual cap.

*(calls `search_knowledge` with query="France speaker fee annual limit configuration")*:

> **Diagnosis Steps:**
> 1. Check the HCP's year-to-date speaker fee total in the Events module
> 2. Compare against the configured annual limit in Country Rules → France → Events → Speaker Fee Limits
> 3. Verify the limit is set correctly — the default configuration may use an outdated limit
>
> **Common Issue:** The default French speaker fee limit in the cloud platform uses 2022 regulatory amounts. France updated the thresholds in 2024. If your configuration wasn't updated post-migration, the limits may be too low.
>
> **Fix:**
> - Update Country Rules → France → Speaker Fee Annual Limit to the current regulatory amount
> - If the payment is legitimate and within the correct limit, the system will allow it after the configuration update
> - All fees above €10 will still be flagged for Sunshine Act disclosure reporting

**User:**
> One more — the operations agent workflow says we should run a post-go-live audit. What does that look like?

**Assistant** *(calls `get_agent_workflow` with agent="operations")*:

> Here's the operations agent post-go-live audit workflow:
>
> **Phase 1: Data Integrity Check** (Week 1)
> - [ ] Verify migrated record counts match source system
> - [ ] Spot-check 50 records per module for field-level accuracy
> - [ ] Validate all lookup relationships resolved correctly
> - [ ] Confirm no orphaned records (children without parents)
>
> **Phase 2: Configuration Validation** (Week 1-2)
> - [ ] Run all validation rules against production data
> - [ ] Verify country rules are active for all deployed countries
> - [ ] Confirm sample limits match legacy system configuration
> - [ ] Test consent capture and expiry workflows in each country
>
> **Phase 3: User Acceptance** (Week 2-3)
> - [ ] Verify 5 reps per country can complete core workflows
> - [ ] Confirm offline sync works for all modules
> - [ ] Test approved email send and tracking end-to-end
> - [ ] Validate event registration and speaker payment workflows
>
> **Phase 4: Compliance Verification** (Week 3-4)
> - [ ] Run sample compliance reports and compare to legacy
> - [ ] Verify consent records are correctly enforced per country
> - [ ] Confirm transparency reporting captures all required transactions
> - [ ] Test data subject access request workflow (GDPR/APPI)

---

## Tools Used

1. `get_terminology` — Clarified merge field vs. template token terminology
2. `run_validation` — Diagnosed template token object context mismatch
3. `get_country_rules` — Retrieved France-specific speaker fee regulations
4. `search_knowledge` — Found speaker fee limit configuration details
5. `get_agent_workflow` — Retrieved the post-go-live audit checklist
