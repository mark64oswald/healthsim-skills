# NetworkSim Examples

NetworkSim provides healthcare network knowledge and synthetic entity generation. This file demonstrates common use cases.

---

## Quick Reference Examples

### Explain Network Types

**Prompt**:
```
Explain the difference between HMO and PPO networks
```

**Expected Response**:
| Aspect | HMO | PPO |
|--------|-----|-----|
| Network Access | Closed - in-network only | Open - any provider |
| Referrals | Required for specialists | Not required |
| PCP Required | Yes | No |
| Out-of-Network | Emergency only | Covered at higher cost |
| Premiums | Lower | Higher |

---

### Explain Pharmacy Benefit Tiers

**Prompt**:
```
Explain pharmacy benefit tier structures
```

**Expected Response**:
| Tier | Drug Type | Typical Copay |
|------|-----------|---------------|
| Tier 1 | Generic | $10 |
| Tier 2 | Preferred Brand | $35 |
| Tier 3 | Non-Preferred Brand | $60 |
| Tier 4 | Specialty | 25% coinsurance |

---

## Synthetic Provider Examples

### Generate Primary Care Physician

**Prompt**:
```
Generate a primary care physician in Chicago, Illinois
```

**Expected Response**:
```json
{
  "npi": "1234567890",
  "entity_type": "individual",
  "provider": {
    "last_name": "Williams",
    "first_name": "Sarah",
    "credential": "MD"
  },
  "taxonomy": {
    "code": "207R00000X",
    "classification": "Internal Medicine",
    "specialization": null
  },
  "practice_location": {
    "address_line_1": "233 E Erie Street",
    "city": "Chicago",
    "state": "IL",
    "zip": "60611",
    "county_fips": "17031"
  }
}
```

---

### Generate Specialist with Credentials

**Prompt**:
```
Generate an interventional cardiologist in Houston, Texas with full credentials
```

**Expected Response**:
```json
{
  "npi": "1987654321",
  "entity_type": "individual",
  "provider": {
    "last_name": "Patel",
    "first_name": "Vikram",
    "credential": "MD, FACC, FSCAI"
  },
  "taxonomy": {
    "primary": {
      "code": "207RC0001X",
      "classification": "Internal Medicine",
      "specialization": "Interventional Cardiology"
    }
  },
  "practice_location": {
    "city": "Houston",
    "state": "TX",
    "county_fips": "48201"
  },
  "board_certifications": [
    {
      "board": "American Board of Internal Medicine",
      "specialty": "Cardiovascular Disease",
      "certification_date": "2012"
    },
    {
      "board": "American Board of Internal Medicine",
      "specialty": "Interventional Cardiology",
      "certification_date": "2014"
    }
  ],
  "hospital_privileges": [
    {"facility_name": "Houston Methodist Hospital", "ccn": "450358"}
  ]
}
```

---

## Synthetic Facility Examples

### Generate Community Hospital

**Prompt**:
```
Generate a 200-bed community hospital in suburban Dallas
```

**Expected Response**:
```json
{
  "ccn": "450XXX",
  "npi": "1234567890",
  "facility": {
    "name": "Plano Community Medical Center",
    "type": "Short Term Acute Care Hospital",
    "subtype": "General Medical and Surgical"
  },
  "characteristics": {
    "bed_count": 200,
    "staffed_beds": 185,
    "emergency_department": true,
    "trauma_level": null,
    "teaching_hospital": false
  },
  "services": {
    "cardiac_surgery": false,
    "cardiac_cath_lab": true,
    "labor_delivery": true,
    "nicu_level": 2
  },
  "location": {
    "city": "Plano",
    "state": "TX",
    "county_fips": "48085"
  }
}
```

---

### Generate Ambulatory Surgery Center

**Prompt**:
```
Generate an ambulatory surgery center specializing in orthopedics in Phoenix
```

**Expected Response**:
```json
{
  "ccn": "03XXXX",
  "facility": {
    "name": "Desert Orthopedic Surgery Center",
    "type": "Ambulatory Surgical Center",
    "specialty_focus": ["Orthopedic Surgery"]
  },
  "characteristics": {
    "operating_rooms": 4,
    "procedure_rooms": 2,
    "overnight_stay": false
  },
  "services": {
    "total_joint": true,
    "arthroscopy": true,
    "spine": false,
    "pain_management": true
  },
  "location": {
    "city": "Phoenix",
    "state": "AZ",
    "county_fips": "04013"
  }
}
```

---

## Synthetic Pharmacy Examples

### Generate Retail Pharmacy

**Prompt**:
```
Generate a CVS pharmacy in San Diego, California
```

**Expected Response**:
```json
{
  "ncpdp_id": "3456789",
  "npi": "1876543210",
  "pharmacy": {
    "name": "CVS Pharmacy #4521",
    "type": "Community/Retail Pharmacy",
    "chain_code": "CVS"
  },
  "services": {
    "immunizations": true,
    "mtm": true,
    "drive_through": true,
    "24_hour": false
  },
  "location": {
    "address_line_1": "1234 Camino Del Rio North",
    "city": "San Diego",
    "state": "CA",
    "zip": "92108",
    "county_fips": "06073"
  }
}
```

---

### Generate Specialty Pharmacy

**Prompt**:
```
Generate a specialty pharmacy for oncology medications
```

**Expected Response**:
```json
{
  "ncpdp_id": "5678901",
  "pharmacy": {
    "name": "OncoMed Specialty Pharmacy",
    "type": "Specialty Pharmacy",
    "specialty_focus": ["Oncology"]
  },
  "specialty": {
    "specialty_pharmacy": true,
    "therapeutic_areas": ["Solid Tumors", "Hematologic Malignancies"],
    "accreditations": ["URAC", "ACHC"]
  },
  "services": {
    "clinical_pharmacist": true,
    "nurse_support": true,
    "adherence_programs": true,
    "copay_assistance": true,
    "cold_chain": true
  },
  "delivery": {
    "next_day": true,
    "temperature_controlled": true,
    "signature_required": true
  }
}
```

---

## Cross-Product Integration Examples

### Provider for PatientSim Encounter

**Prompt**:
```
Generate a provider for this heart failure patient's cardiology referral

Context:
- Patient diagnosis: I50.9 (Heart failure, unspecified)
- Patient location: Houston, TX
- Referral type: Specialist consultation
```

**Expected Response**:
```json
{
  "encounter_providers": {
    "consulting_provider": {
      "npi": "1987654321",
      "role": "Consulting",
      "provider": {
        "last_name": "Chen",
        "first_name": "Michael",
        "credential": "MD, FACC, FHFSA"
      },
      "taxonomy": {
        "code": "207RC0200X",
        "display_name": "Advanced Heart Failure and Transplant Cardiology"
      },
      "assignment_reason": "Heart failure diagnosis (I50.9) matched to heart failure specialist"
    },
    "integration_metadata": {
      "source_product": "patientsim",
      "matching_logic": "diagnosis_to_specialty"
    }
  }
}
```

---

### Network Status for MemberSim Claim

**Prompt**:
```
Determine network status for this member's claim

Context:
- Member plan: PPO with tiered network
- Provider NPI: 1234567890
- Service: Office visit (99213)
```

**Expected Response**:
```json
{
  "network_status": {
    "status": "IN_NETWORK",
    "tier": {
      "tier_id": "TIER-1",
      "tier_name": "Preferred",
      "tier_level": 1
    },
    "cost_sharing": {
      "copay": 25,
      "deductible_applies": false
    },
    "contracted_rate": 125.00
  }
}
```

---

### Pharmacy Routing for RxMemberSim

**Prompt**:
```
Route this prescription to the appropriate pharmacy

Context:
- Drug: Humira 40mg pen
- Days supply: 28
- Member benefit: Specialty carve-out
```

**Expected Response**:
```json
{
  "pharmacy_assignment": {
    "routing_type": "SPECIALTY",
    "pharmacy": {
      "name": "Accredo Specialty Pharmacy",
      "pharmacy_type": "Specialty",
      "ncpdp_id": "5678901"
    },
    "routing_reason": "Specialty indicator on drug - routed to designated specialty pharmacy",
    "clinical_services": {
      "welcome_call": true,
      "adherence_monitoring": true,
      "side_effect_management": true
    },
    "cost_sharing": {
      "tier": 4,
      "coinsurance": 0.25,
      "max_oop": 400
    }
  }
}
```

---

### Formulary Check for RxMemberSim

**Prompt**:
```
Is this drug covered on the member's formulary?

Context:
- Drug: Atorvastatin 20mg
- Formulary: ESI Standard 2024
```

**Expected Response**:
```json
{
  "formulary_status": {
    "covered": true,
    "formulary_status": "Formulary",
    "tier": {
      "tier_id": 1,
      "tier_name": "Generic"
    },
    "cost_sharing": {
      "copay_retail_30": 10,
      "copay_mail_90": 20
    },
    "clinical_programs": {
      "prior_authorization": false,
      "step_therapy": false,
      "quantity_limit": {
        "applies": true,
        "quantity": 90,
        "per_days": 30
      }
    }
  }
}
```

---

## Network Pattern Examples

### HMO Network Configuration

**Prompt**:
```
Generate an HMO network configuration for Los Angeles County
```

**Expected Response**:
```json
{
  "network": {
    "network_id": "NET-CA-HMO-LA-2024",
    "name": "LA Care HMO Network",
    "type": "HMO",
    "model": "IPA Model"
  },
  "configuration": {
    "pcp_gatekeeper": true,
    "referral_required": true,
    "out_of_network_coverage": "Emergency only",
    "capitation": true
  },
  "panel_management": {
    "pcp_panel_size": 2000,
    "panel_open": true
  },
  "geography": {
    "counties": ["06037"],
    "county_names": ["Los Angeles County"]
  },
  "adequacy": {
    "pcp_count": 2500,
    "specialist_count": 4800,
    "hospital_count": 45
  }
}
```

---

### Tiered PPO Network

**Prompt**:
```
Generate a quality-based tiered PPO network with 3 tiers
```

**Expected Response**:
```json
{
  "network": {
    "network_id": "NET-TX-TIERED-2024",
    "name": "HealthSelect Quality Tiered PPO",
    "type": "PPO",
    "tiered": true
  },
  "tiers": [
    {
      "tier_id": "BLUE",
      "tier_name": "Blue Tier - Preferred",
      "tier_level": 1,
      "criteria": "Top 25% quality score",
      "cost_sharing": {"copay_pcp": 15, "coinsurance": 0.10}
    },
    {
      "tier_id": "WHITE",
      "tier_name": "White Tier - Standard",
      "tier_level": 2,
      "criteria": "50-75% quality score",
      "cost_sharing": {"copay_pcp": 30, "coinsurance": 0.20}
    },
    {
      "tier_id": "GRAY",
      "tier_name": "Gray Tier - Basic",
      "tier_level": 3,
      "criteria": "Below 50% quality score",
      "cost_sharing": {"copay_pcp": 50, "coinsurance": 0.35}
    }
  ],
  "quality_metrics": ["HEDIS measures", "Patient satisfaction", "Cost efficiency"]
}
```

---

## Best Practices Demonstrated

1. **Be specific about geography** - County-level specificity produces realistic entities
2. **Include specialty details** - Specific specialties map to correct taxonomy codes
3. **Provide context for integration** - Cross-product prompts need source context
4. **Request credentials when needed** - Full credentials output requires explicit request
5. **Reference network constraints** - Network type affects valid outputs

---

## Related Examples

- [PatientSim Examples](patientsim-examples.md) - Clinical encounters
- [MemberSim Examples](membersim-examples.md) - Claims and members
- [RxMemberSim Examples](rxmembersim-examples.md) - Pharmacy claims
- [Cross-Domain Examples](cross-domain-examples.md) - Multi-product scenarios

---

*NetworkSim Examples v1.0 - December 2024*
