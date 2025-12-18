---
name: recruitment-enrollment
description: "Recruitment and enrollment patterns for clinical trials including screening funnel, informed consent, eligibility assessment, screen failures, and enrollment. Use when generating realistic recruitment timelines and screening outcomes."
---

# Recruitment and Enrollment Patterns

> **Status:** Placeholder - Full implementation in Phase 2

## Overview

This skill will cover the pre-enrollment recruitment funnel:
- Recruitment sources (referrals, registries, advertising, EHR identification)
- Pre-screening contact and preliminary eligibility
- Informed consent process
- Screening visit and eligibility assessment
- Screen failure reasons and patterns
- Enrollment and baseline establishment

## Planned Entities

| Entity | Description |
|--------|-------------|
| **RecruitmentSource** | Channel that identified potential subject |
| **ScreeningLog** | Tracking all screened individuals |
| **PreScreening** | Initial eligibility check before consent |
| **InformedConsent** | Consent documentation and timing |
| **EligibilityAssessment** | Full I/E criteria evaluation |
| **ScreenFailure** | Failed screening with reasons |

## Planned Content

### Recruitment Sources

- Physician referrals
- Patient registries and databases
- Digital/social media advertising
- EHR-based identification (computable phenotypes)
- Site databases
- Trial matching services

### Screening Funnel Metrics

Typical funnel ratios (Phase III oncology):

| Stage | Drop Rate |
|-------|-----------|
| Pre-screen to Consent | 40-60% |
| Consent to Screen | 5-10% |
| Screen to Randomize | 15-25% |

### Screen Failure Patterns

Common screen failure reasons by category:

**Eligibility-Related:**
- Does not meet I/E criteria
- Disease progression during screening
- Inadequate organ function (labs)

**Subject-Related:**
- Consent withdrawal
- Unable to comply with protocol
- Lost to follow-up

**Site/Sponsor-Related:**
- Enrollment cap reached
- Study terminated
- Administrative reasons

### Timeline Patterns

| Event | Typical Window |
|-------|----------------|
| Pre-screen to Consent | 0-14 days |
| Consent to Screening Visit | 0-7 days |
| Screening Period | 14-28 days |
| Screen to Randomization | 0-7 days |

## Related SDTM Domains

| Domain | Use |
|--------|-----|
| **IE** | Inclusion/Exclusion Criteria Not Met |
| **DS** | Disposition - screen failures |
| **SM** | Subject Milestones |

## Generation Parameters (Planned)

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| screen_failure_rate | float | 0.20 | Proportion failing screening |
| consent_withdrawal_rate | float | 0.05 | Withdrawal before randomization |
| screening_period_days | int | 21 | Screening window |
| recruitment_sources | list | ["referral"] | Active recruitment channels |

## See Also

- [clinical-trials-domain.md](./clinical-trials-domain.md) - Core domain knowledge
- [../scenarios/phase3-pivotal.md](../scenarios/phase3-pivotal.md) - Phase III scenario
