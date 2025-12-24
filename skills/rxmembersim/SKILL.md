---
name: healthsim-rxmembersim
description: "RxMemberSim generates realistic synthetic pharmacy data for testing PBM systems, claims adjudication, and drug utilization review. Use when user requests: (1) pharmacy claims or prescription data, (2) DUR alerts or drug interactions, (3) formulary or tier scenarios, (4) pharmacy prior authorization, (5) NCPDP formatted output."
---

# RxMemberSim - Pharmacy and PBM Data Generation

## For Claude

Use this skill when the user requests pharmacy data, prescription fills, or PBM (Pharmacy Benefit Management) scenarios. This is the primary skill for generating realistic synthetic pharmacy claims and drug utilization data.

**When to apply this skill:**

- User mentions prescriptions, pharmacy claims, or medication fills
- User requests DUR (Drug Utilization Review) alerts or drug interactions
- User specifies formulary, tier, or coverage scenarios
- User asks for NCPDP formatted output
- User needs pharmacy prior authorization or step therapy data

**Key capabilities:**

- Generate pharmacy members with BIN/PCN/Group identifiers
- Create prescription fills (new and refill) with NDC codes
- Model pharmacy claim adjudication and pricing
- Generate DUR alerts (drug interactions, therapeutic duplications, early refills)
- Handle formulary management and tier structures
- Model manufacturer copay programs and patient assistance
- Transform output to NCPDP D.0 format

For specific pharmacy scenarios, load the appropriate scenario skill from the table below.

## Overview

RxMemberSim generates realistic synthetic pharmacy data for testing pharmacy benefit management (PBM) systems, claims adjudication, and drug utilization review. This includes:
- Prescription fills (new and refill)
- Pharmacy claims (NCPDP D.0)
- Drug Utilization Review (DUR) alerts
- Formulary and tier management
- Prior authorization workflows
- Manufacturer copay programs

## Quick Start

### Simple Pharmacy Claim

**Request:** "Generate a pharmacy claim for atorvastatin"

```json
{
  "claim": {
    "claim_id": "RX20250115000001",
    "transaction_code": "B1",
    "service_date": "2025-01-15",
    "ndc": "00071015523",
    "drug_name": "Atorvastatin 20mg",
    "quantity": 30,
    "days_supply": 30,
    "pharmacy_npi": "1234567890"
  },
  "response": {
    "status": "paid",
    "ingredient_cost": 12.50,
    "dispensing_fee": 2.00,
    "copay": 10.00,
    "plan_paid": 4.50
  }
}
```

### DUR Alert Scenario

**Request:** "Generate a pharmacy claim that triggers a drug interaction alert"

Claude loads [dur-alerts.md](dur-alerts.md) and produces a claim with appropriate DUR response.

## Scenario Skills

Load the appropriate scenario based on user request:

| Scenario | Trigger Phrases | File |
|----------|-----------------|------|
| **Retail Pharmacy** | prescription, fill, refill, copay, retail | [retail-pharmacy.md](retail-pharmacy.md) |
| **Specialty Pharmacy** | specialty drug, biologics, limited distribution | [specialty-pharmacy.md](specialty-pharmacy.md) |
| **DUR Alerts** | drug interaction, DUR, therapeutic dup, early refill | [dur-alerts.md](dur-alerts.md) |
| **Formulary Management** | formulary, tier, coverage, preferred | [formulary-management.md](formulary-management.md) |
| **Rx Enrollment** | rx enrollment, pharmacy member, BIN PCN, rx coverage | [rx-enrollment.md](rx-enrollment.md) |
| **Rx Prior Auth** | rx prior auth, pharmacy PA, step therapy, formulary exception | [rx-prior-auth.md](rx-prior-auth.md) |
| **Rx Accumulators** | rx accumulator, pharmacy deductible, rx OOP, TrOOP, Part D phase | [rx-accumulator.md](rx-accumulator.md) |
| **Manufacturer Programs** | copay card, PAP, patient assistance, copay assistance, hub program | [manufacturer-programs.md](manufacturer-programs.md) |

## Generation Parameters

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| fill_type | string | new | new, refill |
| drug_type | string | generic | generic, brand, specialty |
| pharmacy_type | string | retail | retail, mail_order, specialty |
| claim_status | string | paid | paid, rejected, reversed |
| dur_outcome | string | none | none, warning, reject |

## Output Entities

### RxMember
Pharmacy member/cardholder information:
- member_id, cardholder_id
- bin, pcn, group_number, person_code
- rx_plan_code, coverage_start/end
- relationship_code, subscriber_id
- mail_order_eligible, specialty_eligible

### RxPlan
Pharmacy benefit plan configuration:
- rx_plan_code, plan_name, plan_type
- formulary_id, tier_structure
- rx_deductible, rx_oop_max
- specialty settings (coinsurance, per-fill max)
- Part D phases (for Medicare plans)

### RxAccumulator
Pharmacy benefit accumulators:
- rx_deductible (applied, limit, remaining)
- rx_oop_max (applied, limit, remaining)
- specialty_oop, daw_brand_penalty
- TrOOP (for Medicare Part D)
- current_phase (for Part D)

### Prescription
Written prescription details:
- prescription_number, ndc, drug_name
- quantity_prescribed, days_supply
- refills_authorized, refills_remaining
- prescriber_npi, prescriber_dea
- written_date, expiration_date
- daw_code, directions

### PharmacyClaim
NCPDP-style claim transaction:
- claim_id, transaction_code (B1/B2/B3)
- bin, pcn, group_number, cardholder_id
- pharmacy_npi, prescriber_npi
- ndc, quantity_dispensed, days_supply
- pricing fields (ingredient cost, dispensing fee)
- DUR fields (reason, service, result codes)

### ClaimResponse
Adjudication response:
- transaction_response_status (A, R, P, D)
- pricing (ingredient cost paid, dispensing fee, patient pay)
- reject codes (if applicable)
- DUR alerts (if applicable)
- authorization number, accumulated amounts

### PharmacyPriorAuth
Pharmacy PA request and decision:
- pa_id, status, pa_type
- request_date, decision_date
- approval details (override_code, expiration)
- denial details (reason, alternatives)
- clinical information, urgency

### DURAlert
Drug utilization review alert:
- dur_code, dur_type, clinical_significance
- interacting_drugs, severity_level
- override_code, outcome_code
- pharmacist_message, recommendation

### FormularyDrug
Drug coverage information:
- ndc, gpi, drug_name
- tier, covered status
- PA required, step therapy required
- quantity limits, age/gender restrictions

### CopayAssistance
Manufacturer copay programs:
- program_id, program_type
- ndc, program_name
- annual_max_benefit, remaining_benefit
- copay_covered, effective_dates

See [../../references/data-models.md](../../references/data-models.md) for complete schemas.

## NCPDP Transaction Codes

| Code | Description | Use Case |
|------|-------------|----------|
| B1 | Billing | New claim submission |
| B2 | Reversal | Cancel previous claim |
| B3 | Rebill | Correct and resubmit |
| E1 | Eligibility | Check coverage |
| P1 | Prior Auth Request | Submit PA |
| P2 | Prior Auth Inquiry | Check PA status |
| P4 | Prior Auth Cancel | Cancel PA request |

## Common Reject Codes

| Code | Description | Resolution |
|------|-------------|------------|
| 70 | Product/Service Not Covered | Check formulary, PA |
| 75 | Prior Authorization Required | Submit PA request |
| 76 | Plan Limitations Exceeded | Check quantity limits |
| 79 | Refill Too Soon | Wait or override |
| 80 | Prescriber Not Found | Verify NPI |
| 83 | Duplicate Paid Claim | Check claim history |
| 88 | DUR Reject | Clinical review needed |

## DUR Alert Types

| Code | Type | Description |
|------|------|-------------|
| DD | Drug-Drug | Interaction between medications |
| TD | Therapeutic Duplication | Same drug class |
| ER | Early Refill | Before 80% supply used |
| HD | High Dose | Exceeds recommended dose |
| LD | Low Dose | Below therapeutic dose |
| DA | Drug-Age | Age precaution |
| DG | Drug-Gender | Gender precaution |
| DC | Drug-Disease | Contraindication |

## Output Formats

| Format | Request | Use Case |
|--------|---------|----------|
| JSON | default | API testing |
| NCPDP D.0 | "as NCPDP", "pharmacy claim format" | Real-time claims |
| CSV | "as CSV" | Analytics |

See [../../formats/ncpdp-d0.md](../../formats/ncpdp-d0.md) for transformation.

## Examples

### Example 1: Generic Fill - Paid

**Request:** "Generate a paid pharmacy claim for lisinopril"

```json
{
  "member": {
    "member_id": "MEM001234",
    "cardholder_id": "001234001",
    "bin": "610014",
    "pcn": "RXGROUP",
    "group_number": "CORP001"
  },
  "prescription": {
    "prescription_number": "RX78901234",
    "ndc": "00093505601",
    "drug_name": "Lisinopril 10mg Tablet",
    "quantity_prescribed": 30,
    "days_supply": 30,
    "refills_authorized": 5,
    "prescriber_npi": "1234567890",
    "written_date": "2025-01-10"
  },
  "claim": {
    "claim_id": "RX20250115000001",
    "transaction_code": "B1",
    "service_date": "2025-01-15",
    "pharmacy_npi": "9876543210",
    "pharmacy_ncpdp": "1234567",
    "ndc": "00093505601",
    "quantity_dispensed": 30,
    "days_supply": 30,
    "fill_number": 0,
    "daw_code": "0",
    "ingredient_cost_submitted": 8.50,
    "dispensing_fee_submitted": 2.00,
    "usual_customary_charge": 15.00,
    "gross_amount_due": 10.50
  },
  "response": {
    "status": "paid",
    "message": "Claim accepted",
    "ingredient_cost_paid": 8.50,
    "dispensing_fee_paid": 1.75,
    "total_amount_paid": 0.25,
    "patient_pay_amount": 10.00,
    "copay_amount": 10.00,
    "authorization_number": "AUTH20250115001"
  }
}
```

### Example 2: Brand Drug - Rejected (PA Required)

**Request:** "Generate a rejected claim for Eliquis requiring prior auth"

```json
{
  "claim": {
    "claim_id": "RX20250115000002",
    "transaction_code": "B1",
    "service_date": "2025-01-15",
    "ndc": "00003089421",
    "drug_name": "Eliquis 5mg Tablet",
    "quantity_dispensed": 60,
    "days_supply": 30
  },
  "response": {
    "status": "rejected",
    "reject_code": "75",
    "reject_message": "Prior Authorization Required",
    "additional_message": "Submit PA with diagnosis and documentation of AFib or VTE",
    "help_desk_phone": "1-800-555-0123"
  }
}
```

### Example 3: Early Refill Warning

**Request:** "Generate a claim with early refill DUR alert"

```json
{
  "claim": {
    "claim_id": "RX20250115000003",
    "ndc": "00071015523",
    "drug_name": "Atorvastatin 20mg",
    "service_date": "2025-01-15",
    "quantity_dispensed": 30,
    "days_supply": 30
  },
  "response": {
    "status": "paid",
    "dur_response": {
      "alert_count": 1,
      "alerts": [
        {
          "type": "ER",
          "description": "Early Refill",
          "severity": "warning",
          "message": "Refill 8 days early (73% of supply used)",
          "previous_fill_date": "2024-12-27",
          "days_supply_previous": 30,
          "percent_used": 73,
          "professional_service_code": "M0",
          "result_of_service_code": "1A"
        }
      ]
    },
    "patient_pay_amount": 10.00
  }
}
```

### Example 4: Specialty Drug with Copay Assistance

**Request:** "Generate a specialty pharmacy claim with manufacturer copay card"

```json
{
  "claim": {
    "claim_id": "RX20250115000004",
    "ndc": "00074433906",
    "drug_name": "Humira 40mg/0.4mL Pen",
    "quantity_dispensed": 2,
    "days_supply": 28,
    "pharmacy_type": "specialty"
  },
  "response": {
    "status": "paid",
    "ingredient_cost_paid": 6500.00,
    "dispensing_fee_paid": 0.00,
    "patient_pay_amount": 500.00,
    "coinsurance_amount": 500.00,
    "tier": 5
  },
  "copay_assistance": {
    "program_name": "Humira Complete",
    "program_bin": "004682",
    "copay_card_applied": true,
    "assistance_amount": 495.00,
    "final_patient_pay": 5.00,
    "annual_max_benefit": 16000.00,
    "remaining_benefit": 15505.00
  }
}
```

## Related Skills

### RxMemberSim Scenarios
- [retail-pharmacy.md](retail-pharmacy.md) - Standard retail fills
- [specialty-pharmacy.md](specialty-pharmacy.md) - Specialty drug distribution
- [dur-alerts.md](dur-alerts.md) - Drug utilization review
- [formulary-management.md](formulary-management.md) - Formulary and tier structure
- [rx-enrollment.md](rx-enrollment.md) - Pharmacy enrollment and eligibility
- [rx-prior-auth.md](rx-prior-auth.md) - Pharmacy prior authorization
- [rx-accumulator.md](rx-accumulator.md) - Pharmacy accumulator tracking
- [manufacturer-programs.md](manufacturer-programs.md) - Copay cards, PAPs, hub programs

### Cross-Product: PatientSim (Clinical)

RxMemberSim pharmacy claims correspond to PatientSim medication orders:

| RxMemberSim Skill | PatientSim Scenarios | Integration |
|-------------------|---------------------|-------------|
| [retail-pharmacy.md](retail-pharmacy.md) | Chronic disease meds, discharge Rx | Fill date +0-3 days from order/discharge |
| [specialty-pharmacy.md](specialty-pharmacy.md) | Oncology, biologics | Limited distribution, PA often required |
| [dur-alerts.md](dur-alerts.md) | Multi-drug regimens | DDI based on patient's med list |
| [rx-prior-auth.md](rx-prior-auth.md) | High-cost drugs | Clinical criteria from PatientSim |

**PatientSim Scenario Links:**
- [../patientsim/diabetes-management.md](../patientsim/diabetes-management.md) - Oral agents, insulin, GLP-1s
- [../patientsim/heart-failure.md](../patientsim/heart-failure.md) - GDMT medications
- [../patientsim/chronic-kidney-disease.md](../patientsim/chronic-kidney-disease.md) - ESAs, phosphate binders
- [../patientsim/behavioral-health.md](../patientsim/behavioral-health.md) - Psychiatric medications
- [../patientsim/oncology/](../patientsim/oncology/) - Oral oncolytics, supportive care

> **Integration Pattern:** Generate medication orders in PatientSim, then use RxMemberSim to model pharmacy fills. Match NDCs, use appropriate fill timing (retail: same day; specialty: +1-7 days), and apply formulary/PA rules.

### Cross-Product: MemberSim (Claims)

Pharmacy and medical benefits are often coordinated:

| RxMemberSim Skill | MemberSim Skill | Integration |
|-------------------|-----------------|-------------|
| [formulary-management.md](formulary-management.md) | [plan-benefits.md](../membersim/plan-benefits.md) | Coordinated benefit design |
| [rx-accumulator.md](rx-accumulator.md) | [accumulator-tracking.md](../membersim/accumulator-tracking.md) | Combined deductible/OOP |
| [rx-prior-auth.md](rx-prior-auth.md) | [prior-authorization.md](../membersim/prior-authorization.md) | Pharmacy vs. medical PA |
| [rx-enrollment.md](rx-enrollment.md) | [enrollment-eligibility.md](../membersim/enrollment-eligibility.md) | Synchronized coverage |

> **Integration Pattern:** For integrated medical+Rx plans, pharmacy costs count toward combined OOP maximum. Ensure coverage dates and accumulator totals are synchronized.

### Cross-Product: PopulationSim (Demographics & SDOH) - v2.0 Data Integration

PopulationSim v2.0 provides **embedded real-world data** for realistic medication utilization modeling. When a geography is specified, RxMemberSim uses actual CDC PLACES, SVI, and ADI data to ground prescribing patterns, adherence behaviors, and formulary utilization.

#### Data-Driven Generation Pattern

**Step 1: Look up real population data**
```
# For rural Appalachian county - Pike County, KY (FIPS: 21195)
Read from: skills/populationsim/data/county/places_county_2024.csv
→ DIABETES_CrudePrev: 16.8%
→ BPMED_CrudePrev: 62.1% (on BP medication)
→ ACCESS2_CrudePrev: 9.1% (uninsured)

Read from: skills/populationsim/data/county/svi_county_2022.csv
→ RPL_THEMES (overall SVI): 0.91 (very high vulnerability)
→ EP_POV150: 38.2% (below 150% poverty)
→ EP_NOVEH: 8.4% (no vehicle - affects pharmacy access)
```

**Step 2: Apply rates to pharmacy generation**
```json
{
  "cohort_parameters": {
    "geography": { "county_fips": "21195", "name": "Pike County, KY" },
    "expected_drug_classes": {
      "antidiabetics": 0.168,
      "antihypertensives": 0.621
    },
    "adherence_context": {
      "svi_overall": 0.91,
      "transportation_barrier": 0.084,
      "poverty_rate": 0.382
    },
    "data_provenance": {
      "source": "CDC_PLACES_2024",
      "data_year": 2022
    }
  }
}
```

**Step 3: Generate pharmacy claims matching real patterns**
- ~17% of members on antidiabetics (not generic 10%)
- High SVI → higher generic utilization (cost sensitivity)
- Transportation barriers → more mail-order, 90-day fills
- Lower adherence rates (MPR ~0.70 vs 0.80 baseline)

#### Embedded Data Sources for Rx Patterns

| Source | File | Use in RxMemberSim |
|--------|------|-------------------|
| CDC PLACES County | `populationsim/data/county/places_county_2024.csv` | Medication class utilization (BPMED, etc.) |
| CDC PLACES Tract | `populationsim/data/tract/places_tract_2024.csv` | Neighborhood prescribing patterns |
| SVI County | `populationsim/data/county/svi_county_2022.csv` | Adherence modeling, generic preference |
| SVI Tract | `populationsim/data/tract/svi_tract_2022.csv` | Pharmacy access patterns |
| ADI Block Group | `populationsim/data/block_group/adi_blockgroup_2023.csv` | Deprivation → adherence correlation |

#### SDOH Impact on Pharmacy Utilization

| SDOH Factor | Pharmacy Impact | Data Source |
|-------------|-----------------|-------------|
| High SVI (>0.75) | +15% generic utilization, -15% adherence | SVI RPL_THEMES |
| No vehicle (EP_NOVEH) | +20% mail-order preference | SVI tract data |
| High poverty (EP_POV150) | Higher copay card utilization | SVI county data |
| High ADI (>75 percentile) | More early refill rejections | ADI block group |

#### Example: Data-Grounded Diabetic Pharmacy Claims

**Request:** "Generate pharmacy claims for a diabetic population in Pike County, KY"

**Data Lookup:**
```
From places_county_2024.csv (FIPS 21195):
  DIABETES_CrudePrev: 16.8%
  OBESITY_CrudePrev: 41.2%
  BPMED_CrudePrev: 62.1%

From svi_county_2022.csv (FIPS 21195):
  RPL_THEMES: 0.91 (very high vulnerability)
  EP_POV150: 38.2%
  EP_NOVEH: 8.4%
```

**Applied to Generation:**
- Drug mix: 70% metformin (generic), 20% sulfonylureas, 10% GLP-1/SGLT2
- Adherence: MPR ~0.68 (below national average due to high SVI)
- Channel: 65% retail, 35% mail-order (transport barriers)
- Copay programs: 25% utilizing manufacturer assistance

**Output with Provenance:**
```json
{
  "pharmacy_claims": [ ... ],
  "generation_context": {
    "geography": "Pike County, KY (21195)",
    "data_sources": ["CDC_PLACES_2024", "CDC_SVI_2022"],
    "rates_applied": {
      "diabetes_prevalence": 0.168,
      "svi_adherence_modifier": -0.15
    }
  }
}
```

> **Key Principle:** When geography is specified, ground pharmacy claims in real PopulationSim data. This enables realistic medication adherence modeling, generic utilization patterns, and SDOH-influenced pharmacy access behaviors.

### Output Formats
- [../../formats/ncpdp-d0.md](../../formats/ncpdp-d0.md) - NCPDP D.0 format
- [../../formats/csv.md](../../formats/csv.md) - CSV export
- [../../formats/sql.md](../../formats/sql.md) - SQL export

### Reference Data
- [../../references/data-models.md](../../references/data-models.md) - Entity schemas
- [../../references/code-systems.md](../../references/code-systems.md) - NDC, GPI, NCPDP codes
