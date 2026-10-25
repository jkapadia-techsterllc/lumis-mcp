# Example: Regulatory Compliance Check

A compliance officer asks Claude about GDPR implications for their CRM migration to the target platform.

## Conversation

**User:** We're migrating from our legacy CRM to the new platform. We operate in 12 EU countries and Japan. What are the regulatory compliance requirements for the consent data migration?

**Claude:** *(calls `get_country_rules` with country="EU" module="consent")*
*(calls `get_country_rules` with country="Japan" module="consent")*
*(calls `traverse_decision_tree` with tree_name="regulatory-compliance")*

Based on your multi-jurisdiction footprint, here are the critical requirements:

### EU (GDPR) — Critical

1. **Explicit opt-in required**: You cannot migrate legacy consent records with a default "opted in" status unless you have documented evidence of explicit consent. For any records where consent was implied or assumed, set the status to "Not Captured" in the target platform.

2. **Consent expiration tracking**: GDPR requires consent renewal. Configure the target platform with consent expiration periods per purpose. Legacy systems often don't track expiration — you'll need to calculate it from the original consent date.

3. **Right to erasure**: The target platform must be able to completely erase an individual's data on request. Test this workflow before go-live.

4. **Data Protection Impact Assessment**: Conduct a DPIA before starting the migration. The cross-border nature of your operation makes this mandatory.

### Japan (APPI) — High

1. **Cross-border transfer consent**: APPI requires specific consent for transferring personal data outside Japan to countries without adequate data protection. If your target platform is hosted outside Japan, you need this consent.

2. **Purpose specification**: Each consent record must be linked to a specific purpose of use. Verify that legacy consent purposes align with your target platform categories.

### Multi-Jurisdiction Strategy

Since you operate in 13 countries, apply the **most restrictive rule** as your baseline:
- GDPR's explicit opt-in is your default globally
- Configure country-specific overrides only where local law is more permissive
- Build a compliance validation step that runs after every data load to flag records that don't meet their country's requirements

### Recommended Actions

1. Engage legal counsel in your top 3 markets before finalizing consent migration rules
2. Run the consent validation rule (`val-dm-003`) after every trial migration
3. Plan for a re-consent campaign for any records that can't be migrated with verified consent status

**User:** What about sample management? We have PDMA compliance requirements.

**Claude:** *(calls `get_gotchas` with module="Sample Management")*
*(calls `run_validation` with symptom="sample audit trail migration")*

PDMA requires a **complete, unbroken audit trail** for every sample transaction. Here's what that means for your migration:

### Non-Negotiable Requirements

- **Every transaction migrates**: Unlike visits or orders where you can migrate only recent data, sample transactions must be migrated in their entirety. You cannot selectively migrate.
- **Audit chain integrity**: Each sample must be traceable from receipt → inventory → disbursement → HCP acknowledgment. Run the audit trail completeness validation after migration.
- **Lot expiration enforcement**: Every sample lot must have a valid expiration date. Expired lots must be marked as such and blocked from new transactions.
- **HCP signatures preserved**: Electronic signatures on sample receipts are regulatory records. They must migrate as digital assets linked to the correct transaction.

### Known Gap

The legacy CRM enforces sample limits in real-time. The target platform uses a batch-based calculation engine. Between batch runs, a rep could theoretically exceed their limit. Mitigate by:
1. Increasing batch frequency to every 4 hours
2. Adding a trigger-based soft warning when reps approach limits
3. Training reps on the behavior difference

Run validation rule `val-dm-002` (Sample Transaction Audit Trail Completeness) after each trial migration to verify zero gaps.
