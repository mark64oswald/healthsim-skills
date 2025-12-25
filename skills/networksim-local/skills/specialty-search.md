---
name: Specialty Search
description: Find providers by medical specialty using taxonomy codes. Trigger phrases include "find cardiologists", "search for specialists", "doctors specializing in", "find a [specialty]"
version: 1.0.0
status: active
product: networksim-local
related_skills:
  - provider-lookup
  - geographic-search
  - facility-lookup
---

# Specialty Search

Find providers by medical specialty using NUCC taxonomy codes.

## Overview

Search the NPPES registry for providers with specific specialties:
- Medical specialties (cardiology, oncology, etc.)
- Surgical specialties
- Primary care
- Mental health
- Allied health (PT, OT, etc.)

## Trigger Phrases

- "Find cardiologists in [location]"
- "Search for orthopedic surgeons"
- "Doctors specializing in [specialty]"
- "Find a dermatologist near [location]"
- "Primary care providers in [city]"

## Parameters

| Parameter | Required | Type | Description |
|-----------|----------|------|-------------|
| specialty | Required | String | Specialty name or taxonomy code |
| state | Optional | String | 2-letter state code |
| city | Optional | String | City name |
| limit | Optional | Integer | Max results (default: 50) |

## Common Taxonomy Codes

| Specialty | Taxonomy Code | Category |
|-----------|---------------|----------|
| Internal Medicine | 207R00000X | Allopathic Physicians |
| Cardiology | 207RC0000X | Internal Medicine |
| Family Medicine | 207Q00000X | Allopathic Physicians |
| Pediatrics | 208000000X | Allopathic Physicians |
| Orthopedic Surgery | 207X00000X | Allopathic Physicians |
| General Surgery | 208600000X | Allopathic Physicians |
| Psychiatry | 2084P0800X | Psychiatry & Neurology |
| Neurology | 2084N0400X | Psychiatry & Neurology |
| Emergency Medicine | 207P00000X | Allopathic Physicians |
| OB/GYN | 207V00000X | Allopathic Physicians |
| Dermatology | 207N00000X | Allopathic Physicians |
| Ophthalmology | 207W00000X | Allopathic Physicians |
| Nurse Practitioner | 363L00000X | Advanced Practice Nursing |
| Physician Assistant | 363A00000X | Physician Assistants |
| Physical Therapist | 225100000X | Rehabilitative |
| Pharmacist | 1835G0000X | Pharmacy Service |

## Query Patterns

### By Taxonomy Code (Exact)

```sql
SELECT npi, 
       COALESCE(organization_name, last_name || ', ' || first_name) as provider_name,
       credential, taxonomy_code, practice_city, practice_state, practice_phone
FROM providers 
WHERE taxonomy_code = '207RC0000X'  -- Cardiology
LIMIT 100;
```

### By Taxonomy Prefix (Specialty Group)

```sql
-- All internal medicine subspecialties
SELECT npi, 
       COALESCE(organization_name, last_name || ', ' || first_name) as provider_name,
       credential, taxonomy_code, practice_city, practice_state
FROM providers 
WHERE taxonomy_code LIKE '207R%'
LIMIT 100;
```

### By Specialty in Location

```sql
SELECT npi, 
       COALESCE(organization_name, last_name || ', ' || first_name) as provider_name,
       credential, taxonomy_code, practice_address_1, practice_city, practice_zip, practice_phone
FROM providers 
WHERE taxonomy_code LIKE '207RC%'  -- Cardiology
  AND practice_state = 'CA'
ORDER BY practice_city
LIMIT 100;
```

## Examples

### Example 1: Specialty by State

**User**: Find cardiologists in California

**Response**:
```
Found 4,892 cardiologists (207RC0000X) in California

Top Cities:
  Los Angeles: 1,234
  San Francisco: 567
  San Diego: 456
  Sacramento: 234

Sample Providers:
1. Chen, William MD FACC - NPI: 1234567890
   Cardiovascular Disease | Los Angeles, CA 90024
   (310) 555-1234
   
2. Rodriguez, Maria MD - NPI: 2345678901
   Cardiovascular Disease | San Diego, CA 92103
   (619) 555-5678

3. Kim, David DO - NPI: 3456789012
   Cardiovascular Disease | San Francisco, CA 94102
   (415) 555-9012

Source: NPPES Registry, December 2024
```

### Example 2: Primary Care Search

**User**: Find primary care doctors in Austin, TX

**Response**:
```
Found 2,345 primary care providers in Austin, TX

By Specialty:
  Family Medicine (207Q): 1,234
  Internal Medicine (207R): 567
  Pediatrics (2080): 345
  Nurse Practitioners (363L): 199

Sample Providers:
1. Johnson, Sarah MD - NPI: 1122334455
   Family Medicine | 123 Main St, Austin, TX 78701
   
2. Williams, Michael DO - NPI: 2233445566
   Internal Medicine | 456 Oak Blvd, Austin, TX 78702

Source: NPPES Registry, December 2024
```

### Example 3: Mental Health Providers

**User**: Find psychiatrists in New York City

**Response**:
```
Found 3,456 psychiatrists (2084P0800X) in New York, NY

By Borough (approximate by ZIP):
  Manhattan (100xx): 1,876
  Brooklyn (112xx): 654
  Queens (113xx): 432
  Bronx (104xx): 234
  Staten Island (103xx): 123

Sample Providers:
1. Goldman, Rachel MD - NPI: 1234567890
   Psychiatry | 123 Park Ave, New York, NY 10016

Source: NPPES Registry, December 2024
```

## Specialty Categories

### Physicians (Allopathic & Osteopathic)
- Prefix `207*`: Most MD specialties
- Prefix `208*`: Pediatrics, Surgery, Urology
- Prefix `204*`: Osteopathic specialties

### Advanced Practice
- `363L*`: Nurse Practitioners
- `363A*`: Physician Assistants

### Mental Health
- `2084P*`: Psychiatry
- `1041*`: Psychology
- `101Y*`: Counselors

### Allied Health
- `225*`: Physical Therapy
- `225X*`: Occupational Therapy
- `231*`: Audiology
- `235*`: Speech-Language Pathology

## Validation Rules

1. Taxonomy codes must be valid NUCC codes
2. Common specialty names are mapped to taxonomy codes
3. Results limited to active providers
4. Can combine with geographic filters

## Related Skills

- [Provider Lookup](provider-lookup.md) - Look up by NPI
- [Geographic Search](geographic-search.md) - Find by location
- [Facility Lookup](facility-lookup.md) - Find hospitals/facilities
