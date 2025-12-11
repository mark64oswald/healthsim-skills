---
name: healthsim-membersim
description: "MemberSim generates realistic synthetic claims and payer data for testing claims processing systems, payment integrity, and benefits administration."
---

# MemberSim - Claims and Payer Data Generation

## Overview

MemberSim generates realistic synthetic claims and payer data for testing claims processing systems, payment integrity, and benefits administration. This includes:
- Member enrollment and eligibility
- Professional claims (837P)
- Institutional/facility claims (837I)
- Claim adjudication and payment
- Prior authorization workflows
- Accumulator tracking (deductible, OOP)

## Quick Start

### Simple Professional Claim

**Request:** "Generate a professional claim for an office visit"

```json
{
  "claim": {
    "claim_id": "CLM20250115000001",
    "claim_type": "PROFESSIONAL",
    "member_id": "MEM001234",
    "provider_npi": "1234567890",
    "service_date": "2025-01-15",
    "place_of_service": "11",
    "principal_diagnosis": "I10",
    "claim_lines": [
      {
        "line_number": 1,
        "procedure_code": "99214",
        "charge_amount": 175.00,
        "units": 1
      }
    ]
  },
  "adjudication": {
    "status": "paid",
    "allowed_amount": 125.00,
    "paid_amount": 100.00,
    "copay": 25.00
  }
}
```

### Facility Claim with DRG

**Request:** "Generate an inpatient claim for heart failure admission"

Claude loads [facility-claims.md](facility-claims.md) and produces a complete 837I-style claim with DRG assignment.

## Scenario Skills

Load the appropriate scenario based on user request:

| Scenario | Trigger Phrases | File |
|----------|-----------------|------|
| **Plan & Benefits** | plan, benefit plan, HMO, PPO, HDHP, copay, deductible structure | [plan-benefits.md](plan-benefits.md) |
| **Enrollment & Eligibility** | enrollment, eligibility, 834, 270, 271, coverage | [enrollment-eligibility.md](enrollment-eligibility.md) |
| **Professional Claims** | office visit, 837P, physician claim, E&M | [professional-claims.md](professional-claims.md) |
| **Facility Claims** | hospital, inpatient, 837I, DRG, UB-04 | [facility-claims.md](facility-claims.md) |
| **Prior Authorization** | prior auth, pre-cert, authorization, PA | [prior-authorization.md](prior-authorization.md) |
| **Accumulator Tracking** | deductible, OOP, accumulator, cost sharing | [accumulator-tracking.md](accumulator-tracking.md) |
| **Value-Based Care** | quality measures, VBC, HEDIS, risk adjustment, HCC, care gaps | [value-based-care.md](value-based-care.md) |
| **Behavioral Health** | mental health, psychiatry, psychotherapy, substance abuse, SUD | [behavioral-health.md](behavioral-health.md) |

## Generation Parameters

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| claim_type | string | PROFESSIONAL | PROFESSIONAL, INSTITUTIONAL, DENTAL |
| claim_status | string | paid | paid, denied, pending, partial |
| network_status | string | in-network | in-network, out-of-network |
| member_age | int or range | 18-65 | Member age |
| plan_type | string | PPO | HMO, PPO, EPO, POS, HDHP |

## Output Entities

### Member
Extends Person with coverage information:
- member_id, subscriber_id, relationship_code
- group_id, plan_code
- coverage_start, coverage_end
- PCP assignment (for HMO)

### Claim
Claim header with:
- claim_id, claim_type
- member_id, provider_npi
- service dates, place of service
- diagnosis codes (principal + secondary)
- claim_lines array

### ClaimLine
Individual service line:
- procedure_code (CPT/HCPCS)
- modifiers, units
- charge_amount
- revenue_code (for institutional)

### Adjudication
Payment determination:
- status (paid, denied, pending)
- allowed_amount, paid_amount
- deductible, copay, coinsurance
- adjustment_reason_codes

### Plan
Benefit plan configuration:
- plan_type (HMO, PPO, etc.)
- deductibles, OOP maximums
- copays, coinsurance rates
- network requirements

### Accumulator
Year-to-date cost sharing:
- deductible_applied vs deductible_limit
- oop_applied vs oop_limit
- Family vs individual tracking

See [../../references/data-models.md](../../references/data-models.md) for complete schemas.

## Adjudication Logic

### Payment Calculation
```
1. Verify eligibility (coverage active on service date)
2. Check network status (in-network vs OON)
3. Determine allowed amount (fee schedule or % of charges)
4. Apply cost sharing:
   a. Deductible (if not met)
   b. Copay (fixed amount)
   c. Coinsurance (% of allowed after deductible)
5. Calculate paid amount = allowed - member responsibility
6. Update accumulators
```

### Common Denial Reasons
| Code | Description | Scenario |
|------|-------------|----------|
| CO-4 | Procedure code inconsistent with modifier | Invalid modifier |
| CO-45 | Charge exceeds fee schedule | UCR violation |
| CO-50 | Non-covered services | Benefit exclusion |
| CO-96 | Non-covered charge(s) | Out of network, no OON benefit |
| CO-97 | Benefit included in another service | Bundling |
| PR-1 | Deductible amount | Member responsibility |
| PR-2 | Coinsurance amount | Member responsibility |
| PR-3 | Copay amount | Member responsibility |

## Output Formats

| Format | Request | Use Case |
|--------|---------|----------|
| JSON | default | API testing |
| X12 834 | "as 834", "X12 enrollment" | Enrollment file |
| X12 270 | "as 270", "eligibility inquiry" | Eligibility request |
| X12 271 | "as 271", "eligibility response" | Eligibility response |
| X12 837P | "as 837P", "X12 professional" | Claims submission |
| X12 837I | "as 837I", "X12 institutional" | Facility claims |
| X12 835 | "as 835", "remittance" | Payment posting |
| CSV | "as CSV" | Analytics |
| SQL | "as SQL" | Database loading |

See [../../formats/](../../formats/) for transformation skills.

## Examples

### Example 1: Paid Office Visit

**Request:** "Generate a paid claim for a 99214 office visit for hypertension"

```json
{
  "member": {
    "member_id": "MEM001234",
    "name": { "given_name": "Sarah", "family_name": "Johnson" },
    "birth_date": "1978-06-15",
    "gender": "F",
    "plan_code": "PPO-GOLD",
    "coverage_start": "2024-01-01"
  },
  "claim": {
    "claim_id": "CLM20250115000001",
    "claim_type": "PROFESSIONAL",
    "member_id": "MEM001234",
    "provider_npi": "1234567890",
    "service_date": "2025-01-15",
    "place_of_service": "11",
    "principal_diagnosis": "I10",
    "claim_lines": [
      {
        "line_number": 1,
        "procedure_code": "99214",
        "charge_amount": 175.00,
        "units": 1,
        "diagnosis_pointers": [1]
      }
    ]
  },
  "adjudication": {
    "status": "paid",
    "allowed_amount": 125.00,
    "deductible": 0.00,
    "copay": 25.00,
    "coinsurance": 0.00,
    "paid_amount": 100.00,
    "patient_responsibility": 25.00
  }
}
```

### Example 2: Denied Claim (Prior Auth Required)

**Request:** "Generate a denied claim for MRI without prior authorization"

```json
{
  "claim": {
    "claim_id": "CLM20250115000002",
    "claim_type": "PROFESSIONAL",
    "service_date": "2025-01-15",
    "place_of_service": "22",
    "principal_diagnosis": "M54.5",
    "claim_lines": [
      {
        "line_number": 1,
        "procedure_code": "72148",
        "charge_amount": 1500.00,
        "units": 1
      }
    ]
  },
  "adjudication": {
    "status": "denied",
    "denial_reason": "CO-15",
    "denial_message": "Prior authorization required",
    "allowed_amount": 0.00,
    "paid_amount": 0.00
  }
}
```

### Example 3: Partial Payment (Deductible Applied)

**Request:** "Generate a claim where deductible applies"

```json
{
  "accumulator_before": {
    "deductible_applied": 200.00,
    "deductible_limit": 500.00,
    "oop_applied": 200.00,
    "oop_limit": 3000.00
  },
  "claim": {
    "claim_id": "CLM20250115000003",
    "procedure_code": "99214",
    "charge_amount": 175.00
  },
  "adjudication": {
    "status": "paid",
    "allowed_amount": 125.00,
    "deductible": 125.00,
    "copay": 0.00,
    "paid_amount": 0.00,
    "patient_responsibility": 125.00
  },
  "accumulator_after": {
    "deductible_applied": 325.00,
    "deductible_limit": 500.00,
    "oop_applied": 325.00,
    "oop_limit": 3000.00
  }
}
```

### Example 4: Oncology Infusion Claim

**Request:** "Generate a facility claim for chemotherapy infusion"

```json
{
  "claim": {
    "claim_id": "CLM20250115000004",
    "claim_type": "INSTITUTIONAL",
    "member_id": "MEM005678",
    "provider_npi": "1234567890",
    "facility_type": "outpatient_hospital",
    "service_date": "2025-01-15",
    "principal_diagnosis": "C50.911",
    "diagnosis_description": "Malignant neoplasm of right female breast",
    "claim_lines": [
      {
        "line_number": 1,
        "revenue_code": "0335",
        "procedure_code": "96413",
        "hcpcs_code": "J9267",
        "description": "Paclitaxel injection, 1mg",
        "units": 175,
        "charge_amount": 3500.00
      },
      {
        "line_number": 2,
        "revenue_code": "0335",
        "procedure_code": "96415",
        "description": "Chemotherapy infusion, additional hour",
        "units": 2,
        "charge_amount": 400.00
      },
      {
        "line_number": 3,
        "revenue_code": "0250",
        "procedure_code": "96360",
        "hcpcs_code": "J2405",
        "description": "Ondansetron injection (antiemetic)",
        "units": 8,
        "charge_amount": 120.00
      }
    ]
  },
  "prior_auth": {
    "auth_number": "PA20250101-12345",
    "status": "approved",
    "approved_units": 6,
    "approved_through": "2025-06-30"
  },
  "adjudication": {
    "status": "paid",
    "allowed_amount": 3200.00,
    "deductible": 0.00,
    "coinsurance": 640.00,
    "paid_amount": 2560.00,
    "patient_responsibility": 640.00
  }
}
```

Key oncology claim elements:
- J-codes for injectable drugs (J9267 = paclitaxel)
- Revenue code 0335 (chemotherapy)
- Prior authorization reference
- Multi-line claim (drug + administration + supportive care)

## Related Skills

### MemberSim Scenarios
- [plan-benefits.md](plan-benefits.md) - Plan configuration and benefit structure
- [enrollment-eligibility.md](enrollment-eligibility.md) - Enrollment and eligibility
- [professional-claims.md](professional-claims.md) - Professional claim details
- [facility-claims.md](facility-claims.md) - Institutional claim details
- [prior-authorization.md](prior-authorization.md) - PA workflows (includes oncology PAs)
- [accumulator-tracking.md](accumulator-tracking.md) - Cost sharing tracking
- [value-based-care.md](value-based-care.md) - VBC, HEDIS, risk adjustment

### Cross-Product: PatientSim Oncology
- [../patientsim/oncology/](../patientsim/oncology/) - Clinical oncology patient generation
- [../patientsim/oncology/breast-cancer.md](../patientsim/oncology/breast-cancer.md) - Breast cancer clinical data
- [../patientsim/oncology/lung-cancer.md](../patientsim/oncology/lung-cancer.md) - Lung cancer clinical data
- [../patientsim/oncology/colorectal-cancer.md](../patientsim/oncology/colorectal-cancer.md) - Colorectal cancer clinical data

### Cross-Product: RxMemberSim
- [../rxmembersim/specialty-pharmacy.md](../rxmembersim/specialty-pharmacy.md) - Oral oncolytic claims
- [../rxmembersim/rx-prior-auth.md](../rxmembersim/rx-prior-auth.md) - Pharmacy PA for oncology drugs

### Output Formats
- [../../formats/x12-834.md](../../formats/x12-834.md) - X12 enrollment format
- [../../formats/x12-270-271.md](../../formats/x12-270-271.md) - X12 eligibility format
- [../../formats/x12-837.md](../../formats/x12-837.md) - X12 claim format
- [../../formats/x12-835.md](../../formats/x12-835.md) - Remittance format
- [../../formats/csv.md](../../formats/csv.md) - CSV export
- [../../formats/sql.md](../../formats/sql.md) - SQL export

### Reference Data
- [../../references/data-models.md](../../references/data-models.md) - Entity schemas
- [../../references/oncology/](../../references/oncology/) - Oncology codes, medications, regimens
