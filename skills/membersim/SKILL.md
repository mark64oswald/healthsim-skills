---
name: healthsim-membersim
description: "MemberSim generates realistic synthetic claims and payer data for testing claims processing systems, payment integrity, and benefits administration."
---

# MemberSim - Claims and Payer Data Generation

## For Claude

Use this skill when the user requests healthcare claims, payer data, or benefits administration scenarios. This is the primary skill for generating realistic synthetic claims and member data.

**When to apply this skill:**

- User mentions claims, billing, or reimbursement
- User requests 837P (professional) or 837I (facility) claims
- User specifies payer, insurance, or benefits scenarios
- User asks for X12 formatted output (834, 835, 837, 270/271)
- User needs member enrollment, eligibility, or prior authorization data

**Key capabilities:**

- Generate members with coverage and benefit plans
- Create professional and facility claims with proper coding
- Model claim adjudication with CARC codes and payment calculations
- Track accumulators (deductible, OOP, coinsurance)
- Handle prior authorization workflows
- Transform output to X12 formats (837, 835, 834, 270/271)

For specific claims scenarios, load the appropriate scenario skill from the table below.

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

### Cross-Product: PatientSim (Clinical)

MemberSim claims correspond to PatientSim clinical encounters:

| MemberSim Skill | PatientSim Scenarios | Integration |
|-----------------|---------------------|-------------|
| [professional-claims.md](professional-claims.md) | Office visits, consults | Match E&M codes to encounter complexity |
| [facility-claims.md](facility-claims.md) | Inpatient, ED, surgery | Match DRG to admission diagnoses |
| [prior-authorization.md](prior-authorization.md) | Elective procedures | PA approved → procedure scheduled |
| [behavioral-health.md](behavioral-health.md) | Psychiatric care | Match visit types and diagnoses |

**PatientSim Scenario Links:**
- [../patientsim/heart-failure.md](../patientsim/heart-failure.md) - HF admission claims
- [../patientsim/diabetes-management.md](../patientsim/diabetes-management.md) - Diabetes office visit claims
- [../patientsim/elective-joint.md](../patientsim/elective-joint.md) - Surgical episode claims
- [../patientsim/oncology/](../patientsim/oncology/) - Oncology infusion claims
- [../patientsim/behavioral-health.md](../patientsim/behavioral-health.md) - Behavioral health claims

> **Integration Pattern:** Generate clinical encounter in PatientSim first, then use MemberSim to create corresponding claims with matching service dates, diagnosis codes, and procedures.

### Cross-Product: RxMemberSim (Pharmacy)

Medical and pharmacy benefits are often coordinated:

| MemberSim Skill | RxMemberSim Skill | Integration |
|-----------------|-------------------|-------------|
| [plan-benefits.md](plan-benefits.md) | [formulary-management.md](../rxmembersim/formulary-management.md) | Coordinated benefit design |
| [accumulator-tracking.md](accumulator-tracking.md) | [rx-accumulator.md](../rxmembersim/rx-accumulator.md) | Combined deductible/OOP |
| [prior-authorization.md](prior-authorization.md) | [rx-prior-auth.md](../rxmembersim/rx-prior-auth.md) | Medical vs. pharmacy PA |
| [enrollment-eligibility.md](enrollment-eligibility.md) | [rx-enrollment.md](../rxmembersim/rx-enrollment.md) | Synchronized coverage |

> **Integration Pattern:** For integrated medical+Rx benefits, ensure accumulators are synchronized and coverage dates match. Some specialty drugs are covered under medical benefit (infused) vs. pharmacy benefit (oral).

### Cross-Product: PopulationSim (Demographics & SDOH) - v2.0 Data Integration

PopulationSim v2.0 provides **embedded real-world data** for actuarially realistic member generation. When a geography is specified, MemberSim uses actual CDC PLACES, SVI, and ADI data to ground demographics, health patterns, and expected utilization.

#### Data-Driven Generation Pattern

**Step 1: Look up real population data**
```
# For Maricopa County, AZ (FIPS: 04013)
Read from: skills/populationsim/data/county/places_county_2024.csv
→ DIABETES_CrudePrev: 10.2%
→ OBESITY_CrudePrev: 29.8%
→ BPHIGH_CrudePrev: 29.1%
→ ACCESS2_CrudePrev: 12.8% (uninsured rate)

Read from: skills/populationsim/data/county/svi_county_2022.csv
→ RPL_THEMES (overall SVI): 0.52
→ EP_POV150: 18.1% (below 150% poverty)
→ EP_AGE65: 17.2% (65+ population)
```

**Step 2: Apply rates to member generation**
```json
{
  "cohort_parameters": {
    "geography": { "county_fips": "04013", "name": "Maricopa County, AZ" },
    "expected_prevalence": {
      "diabetes": 0.102,
      "obesity": 0.298,
      "hypertension": 0.291
    },
    "demographic_context": {
      "age_65_plus": 0.172,
      "poverty_rate": 0.181
    },
    "data_provenance": {
      "source": "CDC_PLACES_2024",
      "data_year": 2022
    }
  }
}
```

**Step 3: Generate members matching real rates**
- Age distribution mirrors county demographics
- Expected chronic conditions match PLACES prevalence
- Risk scores (HCC) calibrated to population health
- Plan tier selection reflects income distribution

#### Embedded Data Sources

| Source | File | Use in MemberSim |
|--------|------|------------------|
| CDC PLACES County | `populationsim/data/county/places_county_2024.csv` | Expected utilization rates, risk adjustment |
| CDC PLACES Tract | `populationsim/data/tract/places_tract_2024.csv` | Neighborhood-level health patterns |
| SVI County | `populationsim/data/county/svi_county_2022.csv` | SDOH factors, plan selection patterns |
| SVI Tract | `populationsim/data/tract/svi_tract_2022.csv` | Tract-level vulnerability |
| ADI Block Group | `populationsim/data/block_group/adi_blockgroup_2023.csv` | Deprivation-based adherence modeling |

#### PopulationSim Integration Skills

| PopulationSim Skill | MemberSim Application |
|---------------------|----------------------|
| [data-lookup.md](../populationsim/data-access/data-lookup.md) | Exact prevalence rates for risk adjustment |
| [county-profile.md](../populationsim/geographic/county-profile.md) | Service area demographics, health patterns |
| [svi-analysis.md](../populationsim/sdoh/svi-analysis.md) | Social vulnerability → plan tier, adherence |
| [adi-analysis.md](../populationsim/sdoh/adi-analysis.md) | Area deprivation → utilization patterns |
| [cohort-specification.md](../populationsim/cohorts/cohort-specification.md) | Data-driven member panel definition |

#### Example: Data-Grounded Medicare Advantage Panel

**Request:** "Generate 1,000 members for a Medicare Advantage plan in Maricopa County, AZ"

**Data Lookup:**
```
From places_county_2024.csv (FIPS 04013):
  DIABETES_CrudePrev: 10.2%
  CHD_CrudePrev: 6.1%
  COPD_CrudePrev: 6.8%
  KIDNEY_CrudePrev: 2.9%

From svi_county_2022.csv (FIPS 04013):
  RPL_THEMES: 0.52 (moderate vulnerability)
  EP_AGE65: 17.2%
  EP_DISABL: 13.1%
```

**Applied to Generation:**
- ~17% of members are 65+ (matches county rate)
- ~10% have diabetes diagnosis (expected chronic conditions)
- ~6% have CHD (drives HCC scoring)
- SVI 0.52 → moderate plan selection diversity
- Output includes provenance tracking

**Output with Provenance:**
```json
{
  "member_panel": {
    "total_members": 1000,
    "geography": "Maricopa County, AZ (04013)",
    "generation_context": {
      "data_sources": ["CDC_PLACES_2024", "CDC_SVI_2022"],
      "rates_applied": {
        "diabetes": 0.102,
        "chd": 0.061,
        "age_65_plus": 0.172
      }
    }
  }
}
```

> **Key Principle:** When geography is specified, always ground member generation in real PopulationSim data. This enables actuarially realistic synthetic member panels for testing claims systems, risk adjustment, and care management.

### Cross-Product: TrialSim (Clinical Trials)

Members may participate in clinical trials with claims integration:

| MemberSim Context | TrialSim Integration | Claims Impact |
|-------------------|---------------------|---------------|
| Specialty drug coverage | Trial drug provided free | Reduced Rx claims during trial |
| Standard of care | SOC claims continue | Normal claim adjudication |
| Trial-related AEs | May generate medical claims | AE → ED/inpatient claims |

> **Integration Pattern:** When a member enrolls in a trial, standard of care claims continue through MemberSim while trial-specific treatments are tracked in TrialSim. Trial-related adverse events may generate claims.

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
