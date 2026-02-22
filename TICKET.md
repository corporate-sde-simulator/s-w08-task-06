# FINSERV-4264: Refactor SLA alert notification manager

**Status:** In Progress · **Priority:** Medium
**Sprint:** Sprint 30 · **Story Points:** 5
**Reporter:** Ravi Krishnan (SRE Lead) · **Assignee:** You (Intern)
**Due:** End of sprint (Friday)
**Labels:** `backend`, `python`, `sre`, `alerting`
**Task Type:** Code Maintenance

---

## Description

The SLA alert manager monitors service metrics and fires alerts when SLAs are breached. It works but has code quality issues. Refactor without changing behavior.

## Acceptance Criteria

- [ ] Hardcoded SLA thresholds extracted to configuration
- [ ] Alert deduplication logic is unclear — add comments explaining the time-window approach
- [ ] String concatenation for alert messages replaced with f-strings or template
- [ ] Unused `_legacy_check` method removed
- [ ] All tests still pass
