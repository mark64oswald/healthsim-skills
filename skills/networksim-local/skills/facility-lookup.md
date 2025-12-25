---
name: Facility Lookup
description: Find hospitals, clinics, and healthcare facilities by location or type. Trigger phrases include "find hospitals", "clinics in", "healthcare facilities", "medical centers near"
version: 1.0.0
status: active
product: networksim-local
related_skills:
  - provider-lookup
  - geographic-search
  - pharmacy-lookup
---

# Facility Lookup

Find hospitals, clinics, and other healthcare facilities.

## Overview

Search the NPPES registry for healthcare facilities:
- General Acute Care Hospitals
- Critical Access Hospitals
- Psychiatric Hospitals
- Rehabilitation Hospitals
- Ambulatory Surgery Centers
- Clinics (various types)
- Skilled Nursing Facilities
- Home Health Agencies

## Trigger Phrases

- "Find hospitals in [location]"
- "What hospitals are in [city]?"
- "Clinics near [ZIP code]"
- "Healthcare facilities in [state]"
- "Find urgent care in [location]"

## Parameters

| Parameter | Required | Type | Description |
|-----------|----------|------|-------------|
| facility_type | Optional | String | Type of facility |
| state | Conditional | String | 2-letter state code |
| city | Optional | String | City name |
| zip | Conditional | String | ZIP code |

## Facility Types (Taxonomy Codes)

| Facility Type | Taxonomy Prefix | Description |
|---------------|-----------------|-------------|
| Hospital - General | 282N00000X | General acute care hospital |
| Hospital - Critical Access | 282NC0060X | Critical access hospital |
| Hospital - Children's | 282NC2000X | Children's hospital |
| Hospital - Psychiatric | 283Q00000X | Psychiatric hospital |
| Hospital - Rehabilitation | 283X00000X | Rehabilitation hospital |
| Ambulatory Surgery | 261QA1903X | Ambulatory surgery center |
| Urgent Care | 261QU0200X | Urgent care clinic |
| FQHC | 261QF0400X | Federally qualified health center |
| Mental Health Clinic | 261QM0801X | Mental health clinic |
| Dialysis Center | 261QE0700X | ESRD treatment facility |
| Skilled Nursing | 314000000X | Skilled nursing facility |
| Home Health | 251E00000X | Home health agency |

## Query Patterns

### Hospitals by State

```sql
SELECT npi, organization_name, taxonomy_code,
       practice_address_1, practice_city, practice_zip, practice_phone
FROM providers 
WHERE taxonomy_code LIKE '282%'
  AND practice_state = 'CA'
ORDER BY organization_name;
```

### Hospitals by City

```sql
SELECT npi, organization_name, taxonomy_code,
       practice_address_1, practice_zip, practice_phone
FROM providers 
WHERE taxonomy_code LIKE '282N%'  -- General acute care
  AND practice_city ILIKE 'Houston'
  AND practice_state = 'TX'
ORDER BY organization_name;
```

### Clinics by Type

```sql
-- Urgent care clinics
SELECT npi, organization_name,
       practice_address_1, practice_city, practice_state, practice_phone
FROM providers 
WHERE taxonomy_code = '261QU0200X'
  AND practice_state = 'FL'
ORDER BY practice_city;
```

## Examples

### Example 1: Hospitals in State

**User**: What hospitals are in Illinois?

**Response**:
```
Found 456 hospitals in Illinois

By Type:
  General Acute Care: 234
  Critical Access: 89
  Psychiatric: 45
  Rehabilitation: 34
  Children's: 12
  Other: 42

Major Facilities in Chicago:
1. Northwestern Memorial Hospital - NPI: 1234567890
   General Acute Care | 251 E Huron St, Chicago, IL 60611
   
2. Rush University Medical Center - NPI: 2345678901
   General Acute Care | 1653 W Congress Pkwy, Chicago, IL 60612

3. Lurie Children's Hospital - NPI: 3456789012
   Children's Hospital | 225 E Chicago Ave, Chicago, IL 60611

Source: NPPES Registry, December 2024
```

### Example 2: Urgent Care Search

**User**: Find urgent care clinics in San Diego

**Response**:
```
Found 87 urgent care clinics (261QU0200X) in San Diego, CA

Sample Facilities:
1. Sharp Rees-Stealy Urgent Care - NPI: 1122334455
   2001 4th Ave, San Diego, CA 92101
   (619) 555-1234

2. Scripps Clinic Urgent Care - NPI: 2233445566
   10666 N Torrey Pines Rd, La Jolla, CA 92037
   (858) 555-5678

3. UC San Diego Health Urgent Care - NPI: 3344556677
   4510 Executive Dr, San Diego, CA 92121
   (858) 555-9012

Source: NPPES Registry, December 2024
```

### Example 3: Mental Health Facilities

**User**: Mental health clinics in Phoenix, AZ

**Response**:
```
Found 123 mental health clinics (261QM0801X) in Phoenix, AZ

Sample Facilities:
1. Banner Behavioral Health - NPI: 1234567890
   7575 E Earl Dr, Scottsdale, AZ 85251

2. Terros Health - NPI: 2345678901
   2402 E University Dr, Phoenix, AZ 85034

3. Community Bridges Inc - NPI: 3456789012
   1201 S 7th Ave, Phoenix, AZ 85007

Source: NPPES Registry, December 2024
```

## County/Regional Analysis

```sql
-- Hospital count by city in a state
SELECT practice_city, COUNT(*) as hospital_count
FROM providers
WHERE taxonomy_code LIKE '282N%'
  AND practice_state = 'TX'
GROUP BY practice_city
ORDER BY hospital_count DESC
LIMIT 10;
```

## Validation Rules

1. Facility searches require Type 2 (Organization) entities
2. Taxonomy codes determine facility type
3. Results ordered by organization name or city
4. Only active facilities returned

## Cross-Product Integration

**MemberSim**: Use for realistic facility NPIs in claims
```sql
-- Random hospital for claim
SELECT npi, organization_name, practice_city, practice_state
FROM providers 
WHERE taxonomy_code LIKE '282N%' AND practice_state = ?
ORDER BY RANDOM() LIMIT 1;
```

**PatientSim**: Use for service location in encounters
```sql
-- Hospital in patient's area
SELECT npi, organization_name, practice_address_1, practice_city
FROM providers 
WHERE taxonomy_code LIKE '282N%' 
  AND practice_zip LIKE ? || '%'
LIMIT 5;
```

## Related Skills

- [Provider Lookup](provider-lookup.md) - Look up by NPI
- [Geographic Search](geographic-search.md) - Find by location
- [Pharmacy Lookup](pharmacy-lookup.md) - Find pharmacies
