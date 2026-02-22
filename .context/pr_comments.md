# PR Review - SLA breach alerting system (by Sneha Jain)

## Reviewer: Pooja Reddy
---

**Overall:** Good foundation but critical bugs need fixing before merge.

### `slaAlerter.py`

> **Bug #1:** Breach detection runs every hour but SLA window is 15 minutes and misses short breaches
> This is the higher priority fix. Check the logic carefully and compare against the design doc.

### `breachDetector.py`

> **Bug #2:** Alert deduplication uses only ticket ID not breach type so different breaches on same ticket are suppressed
> This is more subtle but will cause issues in production. Make sure to add a test case for this.

---

**Sneha Jain**
> Acknowledged. I have documented the issues for whoever picks this up.
