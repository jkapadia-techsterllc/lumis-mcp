# Example: Validation Rule Audit

A customer's implementation team has reported several post-migration issues. The operations team needs to diagnose the root causes using Lumis's validation and gotcha tools.

---

## Conversation Flow

**User:**
> After our migration, field reps are reporting that sample drop transactions are being rejected with a "limit exceeded" error, but the reps haven't hit their actual limits. What's going on?

**Assistant** *(calls `run_validation` with symptom="sample drop rejected limit exceeded but not at limit")*:

> This matches validation rule **SM-VAL-003: Sample Limit Calculation Period Mismatch**.
>
> **Root Cause:** The legacy CRM calculated sample limits on a rolling 12-month window. The cloud platform defaults to a calendar-year window. If a rep distributed 80% of their limit in November-December of last year (under the legacy rolling window), those transactions now count toward the current calendar year in the new system.
>
> **Diagnosis Steps:**
> 1. Check the rep's sample transaction history for the last 12 months
> 2. Compare the rolling 12-month total vs. the calendar-year total
> 3. If the calendar-year total exceeds the limit but the rolling total doesn't, this is the mismatch
>
> **Fix:**
> Configure the sample limit engine to use a rolling period instead of calendar year:
> - Navigate to Sample Limit Configuration
> - Change "Limit Period Type" from "Calendar Year" to "Rolling Period"
> - Set "Rolling Period Months" to 12
> - Recalculate limits for all affected reps

**User:**
> Good catch. We also have reps in Germany reporting that consent records are showing as "expired" even though the customer gave consent last month.

**Assistant** *(calls `run_validation` with symptom="consent expired recently given Germany")*:

> This matches validation rule **CM-VAL-007: Consent Expiry Default Override Missing**.
>
> **Root Cause:** The cloud platform ships with a default consent expiry of 30 days for GDPR regions. In your legacy CRM, you had configured consent to last 12 months. The migration moved the consent records but not the expiry configuration.
>
> **Diagnosis Steps:**
> 1. Check the consent record's `ConsentGivenDate` and `ExpiryDate` fields
> 2. If `ExpiryDate - ConsentGivenDate = 30 days`, the default is overriding your intended configuration
> 3. Verify the Country Configuration for Germany
>
> **Fix:**
> Update the GDPR country configuration:
> - Navigate to Country Rules → Germany → Consent Management
> - Set "Default Consent Duration" to 365 days (or your intended duration)
> - Run the consent recalculation batch to update existing records

**User:**
> Are there other gotchas we should check proactively for our German deployment?

**Assistant** *(calls `get_gotchas` with country="Germany")*:

> Here are the Germany-specific gotchas to check proactively:
>
> 1. **Double opt-in requirement** — Germany enforces stricter opt-in than baseline GDPR. Ensure your consent capture flow includes a confirmation step (email or in-app). Single opt-in may not be legally sufficient.
>
> 2. **Data residency expectations** — While GDPR allows EU-wide storage, German customers often contractually require data residency within Germany or the EU. Verify your cloud hosting region.
>
> 3. **HCP transparency reporting** — Germany requires disclosure of all transfers of value to healthcare professionals. Ensure sample drop transactions, event sponsorships, and speaker fees are captured in a format compatible with transparency reporting.
>
> 4. **Heilmittelwerbegesetz (HWG) compliance** — German pharmaceutical advertising law restricts what can appear in CLM content. If you're implementing CLM, all content must be reviewed against HWG requirements, not just internal medical-legal review.
>
> 5. **Sunday/holiday rep activity restrictions** — Some German states restrict commercial activities on Sundays and public holidays. If your call reporting tracks visit timestamps, configure alerts for visits logged on restricted days.

---

## Tools Used

1. `run_validation` — Symptom-based diagnosis for sample limit and consent issues
2. `get_gotchas` — Proactive country-specific pitfall discovery for Germany
