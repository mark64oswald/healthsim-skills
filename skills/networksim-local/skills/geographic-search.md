---
name: Geographic Search
description: Find providers by location - city, state, or ZIP code. Trigger phrases include "providers in", "find doctors in", "healthcare in", "medical providers near"
version: 1.0.0
status: active
product: networksim-local
related_skills:
  - provider-lookup
  - specialty-search
  - facility-lookup
---

# Geographic Search

Find real providers by geographic location.

## Overview

Search the NPPES registry for providers in a specific:
- State
- City and State
- ZIP code or ZIP prefix

## Trigger Phrases

- "Find providers in [city], [state]"
- "What doctors are in [state]?"
- "Healthcare providers near ZIP [code]"
- "Medical providers in [city]"
- "Physicians in [location]"

## Parameters

| Parameter | Required | Type | Description |
|-----------|----------|------|-------------|
| state | Conditional | String | 2-letter state code |
| city | Optional | String | City name |
| zip | Conditional | String | ZIP code or prefix |
| entity_type | Optional | String | 'individual' or 'organization' |
| limit | Optional | Integer | Max results (default: 50) |

*Either `state` or `zip` is required*

## Query Patterns

### By State

```sql
SELECT npi, 
       COALESCE(organization_name, last_name || ', ' || first_name) as provider_name,
       credential, taxonomy_code, practice_city, practice_zip
FROM providers 
WHERE practice_state = 'CA'
LIMIT 100;
```

### By City and State

```sql
SELECT npi, 
       COALESCE(organization_name, last_name || ', ' || first_name) as provider_name,
       credential, taxonomy_code, practice_address_1, practice_zip, practice_phone
FROM providers 
WHERE practice_city ILIKE 'San Diego'
  AND practice_state = 'CA'
LIMIT 100;
```

### By ZIP Code

```sql
-- Exact ZIP
SELECT npi, 
       COALESCE(organization_name, last_name || ', ' || first_name) as provider_name,
       credential, taxonomy_code, practice_city, practice_phone
FROM providers 
WHERE practice_zip LIKE '92101%'
LIMIT 100;

-- ZIP prefix (area)
SELECT npi, 
       COALESCE(organization_name, last_name || ', ' || first_name) as provider_name,
       credential, taxonomy_code, practice_city, practice_zip
FROM providers 
WHERE practice_zip LIKE '921%'
LIMIT 100;
```

## Examples

### Example 1: State Search

**User**: How many providers are in Texas?

**Response**:
```
Texas (TX) has 575,858 active providers in the NPPES registry.

Top Cities:
  Houston: 89,432 providers
  Dallas: 56,891 providers
  San Antonio: 38,234 providers
  Austin: 32,876 providers
  Fort Worth: 21,543 providers

Provider Types:
  Physicians: 98,234
  Nurse Practitioners: 23,456
  Pharmacies: 8,901
  Hospitals: 892

Source: NPPES Registry, December 2024
```

### Example 2: City Search

**User**: Find doctors in San Diego, CA

**Response**:
```
Found 12,847 individual providers in San Diego, CA

Sample Results:
1. Johnson, Michael MD - NPI: 1234567890
   Internal Medicine | 123 Medical Center Dr, 92101
   
2. Garcia, Maria DO - NPI: 2345678901
   Family Medicine | 456 Healthcare Blvd, 92103

3. Lee, David MD - NPI: 3456789012
   Cardiology | 789 Heart Way, 92108

[... use specialty search to narrow results]

Source: NPPES Registry, December 2024
```

### Example 3: ZIP Code Search

**User**: Healthcare providers near ZIP 10001

**Response**:
```
Found 3,456 providers in ZIP code 10001 (Manhattan, NY)

By Category:
  Physicians: 1,234
  Clinics: 456
  Pharmacies: 89
  Other: 1,677

Sample Organizations:
1. NYC Health + Hospitals - NPI: 1122334455
   General Acute Care Hospital | 462 1st Ave
   
2. Duane Reade #14321 - NPI: 2233445566
   Community/Retail Pharmacy | 350 5th Ave

Source: NPPES Registry, December 2024
```

## Validation Rules

1. State codes must be valid 2-letter US state/territory codes
2. City names are case-insensitive
3. ZIP codes can be 3-9 characters (prefix matching supported)
4. Results limited to active providers

## State Coverage

The database includes all US states and territories:
- 50 states + DC
- Puerto Rico (PR)
- US Virgin Islands (VI)
- Guam (GU)
- American Samoa (AS)
- Northern Mariana Islands (MP)

## Related Skills

- [Provider Lookup](provider-lookup.md) - Look up by NPI
- [Specialty Search](specialty-search.md) - Find by specialty
- [Facility Lookup](facility-lookup.md) - Find hospitals/facilities
