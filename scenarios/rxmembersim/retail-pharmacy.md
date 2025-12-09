# Retail Pharmacy Scenario

## Trigger Phrases

- retail pharmacy
- prescription fill
- refill
- pharmacy claim
- copay
- CVS
- Walgreens
- pickup
- 30-day supply
- 90-day supply
- mail order

## Parameters

| Parameter | Type | Default | Options |
|-----------|------|---------|---------|
| fill_type | string | new | new, refill |
| days_supply | int | 30 | 30, 60, 90 |
| pharmacy_channel | string | retail | retail, mail_order |
| drug_category | string | generic | generic, preferred_brand, non_preferred_brand |
| claim_status | string | paid | paid, rejected |

## Pharmacy Channels

### Retail Pharmacy
- **Days Supply**: Typically 30 days
- **Copay**: Standard formulary copay
- **Examples**: CVS, Walgreens, Rite Aid, grocery store pharmacies

### Mail Order Pharmacy
- **Days Supply**: Typically 90 days
- **Copay**: Often 2.5x 30-day copay (discount)
- **Use Case**: Maintenance medications

### Preferred Pharmacy Network
- **Copay**: Reduced copay at network pharmacies
- **Non-Preferred**: Higher copay at non-network

## Prescription Lifecycle

```
1. Prescriber writes prescription
   ↓
2. Prescription transmitted to pharmacy (e-prescribe or paper)
   ↓
3. Pharmacist receives and enters prescription
   ↓
4. Pharmacy submits claim to PBM (B1 transaction)
   ↓
5. PBM adjudicates (eligibility, formulary, DUR)
   ↓
6. Response returned (paid, rejected, or warning)
   ↓
7. If paid: Pharmacist dispenses, patient picks up
   ↓
8. Refills available when 75-80% of supply used
```

## Prescription Data Elements

### New Prescription
```json
{
  "prescription_number": "RX{pharmacy_id}{sequence:06d}",
  "ndc": "11-digit NDC",
  "drug_name": "Drug Name Strength Form",
  "quantity_prescribed": 30,
  "days_supply": 30,
  "refills_authorized": 5,
  "daw_code": "0",
  "directions": "Take 1 tablet by mouth daily",
  "prescriber_npi": "10-digit NPI",
  "prescriber_dea": "DEA number (if controlled)",
  "written_date": "YYYY-MM-DD",
  "expiration_date": "YYYY-MM-DD"
}
```

### DAW (Dispense As Written) Codes
| Code | Description | Use Case |
|------|-------------|----------|
| 0 | No product selection indicated | Generic substitution allowed |
| 1 | Substitution not allowed by prescriber | Brand medically necessary |
| 2 | Substitution allowed, patient requested brand | Patient preference |
| 3 | Substitution allowed, pharmacist selected | Pharmacist choice |
| 4 | Substitution allowed, generic not in stock | Supply issue |
| 5 | Brand dispensed as generic | MAC pricing |
| 7 | Substitution not allowed, brand mandated by law | State law |
| 8 | Substitution allowed, generic not available | Market availability |

## Common Drug Categories

### Generic Maintenance Medications
```json
{
  "cardiovascular": [
    { "drug": "Lisinopril 10mg", "ndc": "00093505601", "awp": 8.50, "tier": 1 },
    { "drug": "Atorvastatin 20mg", "ndc": "00071015523", "awp": 12.00, "tier": 1 },
    { "drug": "Metoprolol Succinate 50mg", "ndc": "00378003501", "awp": 15.00, "tier": 1 },
    { "drug": "Amlodipine 5mg", "ndc": "00093231401", "awp": 6.50, "tier": 1 }
  ],
  "diabetes": [
    { "drug": "Metformin 1000mg", "ndc": "00093101901", "awp": 10.00, "tier": 1 },
    { "drug": "Glipizide 10mg", "ndc": "00093108401", "awp": 8.00, "tier": 1 }
  ],
  "mental_health": [
    { "drug": "Sertraline 50mg", "ndc": "00093041801", "awp": 9.00, "tier": 1 },
    { "drug": "Escitalopram 10mg", "ndc": "00093514101", "awp": 11.00, "tier": 1 }
  ]
}
```

### Preferred Brand Medications
```json
{
  "examples": [
    { "drug": "Eliquis 5mg", "ndc": "00003089421", "awp": 520.00, "tier": 3 },
    { "drug": "Jardiance 10mg", "ndc": "00597014130", "awp": 580.00, "tier": 3 },
    { "drug": "Ozempic 1mg/dose", "ndc": "00169410012", "awp": 950.00, "tier": 3 }
  ]
}
```

## Claim Pricing

### Pricing Components
```json
{
  "ingredient_cost": {
    "basis": "AWP, WAC, or MAC",
    "awp_discount": "AWP - 15% to AWP - 20%",
    "mac_list": "Maximum Allowable Cost for generics"
  },
  "dispensing_fee": {
    "retail": "$1.50 - $3.00",
    "mail_order": "$0.00 - $2.00"
  },
  "gross_amount_due": "ingredient_cost + dispensing_fee"
}
```

### Copay by Tier (Commercial Plan)
| Tier | Description | 30-Day Copay | 90-Day Mail |
|------|-------------|--------------|-------------|
| 1 | Preferred Generic | $10 | $25 |
| 2 | Non-Preferred Generic | $25 | $62.50 |
| 3 | Preferred Brand | $50 | $125 |
| 4 | Non-Preferred Brand | $80 | $200 |
| 5 | Specialty | 25% coinsurance | N/A |

## Claim Structure

### NCPDP Claim Request
```json
{
  "header": {
    "bin": "610014",
    "version": "D0",
    "transaction_code": "B1",
    "pcn": "RXGROUP",
    "transaction_count": 1
  },
  "insurance": {
    "cardholder_id": "001234001",
    "group_number": "CORP001",
    "person_code": "01",
    "relationship_code": "1",
    "patient_id": "MEM001234"
  },
  "patient": {
    "date_of_birth": "19780315",
    "patient_gender": "1",
    "patient_first_name": "JOHN",
    "patient_last_name": "SMITH"
  },
  "claim": {
    "prescription_reference_number": "RX78901234",
    "product_service_id": "00093505601",
    "quantity_dispensed": 30.000,
    "days_supply": 30,
    "compound_code": "1",
    "daw_code": "0",
    "date_prescription_written": "20250110",
    "number_of_refills_authorized": 5,
    "prescription_origin_code": "1",
    "fill_number": 0
  },
  "prescriber": {
    "prescriber_id_qualifier": "01",
    "prescriber_id": "1234567890"
  },
  "pharmacy": {
    "service_provider_id_qualifier": "01",
    "service_provider_id": "9876543210"
  },
  "pricing": {
    "ingredient_cost_submitted": 8.50,
    "dispensing_fee_submitted": 2.00,
    "usual_and_customary_charge": 15.00,
    "gross_amount_due": 10.50
  }
}
```

### Claim Response (Paid)
```json
{
  "header": {
    "transaction_response_status": "A",
    "authorization_number": "AUTH20250115001234"
  },
  "pricing": {
    "ingredient_cost_paid": 8.50,
    "dispensing_fee_paid": 1.75,
    "total_amount_paid": 0.25,
    "patient_pay_amount": 10.00,
    "basis_of_reimbursement": "MAC"
  },
  "message": {
    "message": "CLAIM ACCEPTED"
  }
}
```

## Refill Scenarios

### Standard Refill
```json
{
  "original_fill": {
    "prescription_number": "RX78901234",
    "fill_number": 0,
    "service_date": "2024-12-15",
    "days_supply": 30,
    "refills_remaining": 5
  },
  "refill_request": {
    "prescription_number": "RX78901234",
    "fill_number": 1,
    "service_date": "2025-01-12",
    "days_elapsed": 28,
    "percent_used": 93,
    "refills_remaining": 4,
    "status": "eligible"
  }
}
```

### Too Early Refill
```json
{
  "original_fill": {
    "service_date": "2025-01-01",
    "days_supply": 30
  },
  "refill_request": {
    "service_date": "2025-01-15",
    "days_elapsed": 14,
    "percent_used": 47,
    "status": "too_early",
    "earliest_fill_date": "2025-01-25",
    "reject_code": "79"
  }
}
```

## Example Outputs

### Example 1: New Generic Fill

```json
{
  "member": {
    "member_id": "MEM001234",
    "cardholder_id": "001234001",
    "name": { "given_name": "Michael", "family_name": "Brown" },
    "plan_code": "RX-STANDARD"
  },
  "pharmacy": {
    "npi": "9876543210",
    "ncpdp": "1234567",
    "name": "Springfield Pharmacy",
    "address": { "city": "Springfield", "state": "IL" }
  },
  "prescription": {
    "prescription_number": "RX78901234",
    "ndc": "00093505601",
    "drug_name": "Lisinopril 10mg Tablet",
    "quantity_prescribed": 30,
    "days_supply": 30,
    "refills_authorized": 5,
    "directions": "Take 1 tablet by mouth once daily",
    "prescriber_npi": "1234567890",
    "written_date": "2025-01-10"
  },
  "claim": {
    "claim_id": "RX20250115000001",
    "transaction_code": "B1",
    "service_date": "2025-01-15",
    "fill_number": 0,
    "daw_code": "0",
    "ndc": "00093505601",
    "quantity_dispensed": 30,
    "days_supply": 30,
    "ingredient_cost_submitted": 8.50,
    "dispensing_fee_submitted": 2.00
  },
  "response": {
    "status": "paid",
    "authorization_number": "AUTH20250115001234",
    "ingredient_cost_paid": 8.50,
    "dispensing_fee_paid": 1.75,
    "patient_pay_amount": 10.00,
    "copay_amount": 10.00,
    "basis_of_reimbursement": "MAC",
    "formulary_tier": 1,
    "message": "CLAIM ACCEPTED"
  }
}
```

### Example 2: Mail Order 90-Day Supply

```json
{
  "claim": {
    "claim_id": "RX20250115000002",
    "transaction_code": "B1",
    "service_date": "2025-01-15",
    "pharmacy_type": "mail_order",
    "ndc": "00071015523",
    "drug_name": "Atorvastatin 20mg Tablet",
    "quantity_dispensed": 90,
    "days_supply": 90,
    "fill_number": 2,
    "ingredient_cost_submitted": 36.00,
    "dispensing_fee_submitted": 0.00
  },
  "response": {
    "status": "paid",
    "ingredient_cost_paid": 36.00,
    "dispensing_fee_paid": 0.00,
    "patient_pay_amount": 25.00,
    "copay_amount": 25.00,
    "savings_message": "You saved $5.00 using mail order!",
    "formulary_tier": 1
  }
}
```

### Example 3: Brand Drug with Higher Copay

```json
{
  "claim": {
    "claim_id": "RX20250115000003",
    "ndc": "00003089421",
    "drug_name": "Eliquis 5mg Tablet",
    "quantity_dispensed": 60,
    "days_supply": 30,
    "daw_code": "0",
    "ingredient_cost_submitted": 520.00
  },
  "response": {
    "status": "paid",
    "ingredient_cost_paid": 480.00,
    "patient_pay_amount": 50.00,
    "copay_amount": 50.00,
    "formulary_tier": 3,
    "message": "Brand name drug - consider generic alternative if available"
  }
}
```

### Example 4: Rejected - Not Covered

```json
{
  "claim": {
    "claim_id": "RX20250115000004",
    "ndc": "12345678901",
    "drug_name": "Non-Formulary Drug",
    "quantity_dispensed": 30,
    "days_supply": 30
  },
  "response": {
    "status": "rejected",
    "reject_code": "70",
    "reject_message": "Product/Service Not Covered",
    "additional_message": "This drug is not on formulary. Covered alternatives: Drug A, Drug B",
    "formulary_alternatives": [
      { "ndc": "00093505601", "drug_name": "Lisinopril 10mg", "tier": 1, "copay": 10.00 },
      { "ndc": "00378003501", "drug_name": "Metoprolol 50mg", "tier": 1, "copay": 10.00 }
    ]
  }
}
```

## Related Skills

- [SKILL.md](SKILL.md) - RxMemberSim overview
- [specialty-pharmacy.md](specialty-pharmacy.md) - Specialty drug fills
- [dur-alerts.md](dur-alerts.md) - Drug interaction checks
- [formulary-management.md](formulary-management.md) - Tier and coverage
- [../../references/code-systems.md](../../references/code-systems.md) - NDC codes
