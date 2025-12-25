---
name: Pharmacy Lookup
description: Find pharmacies by location or type. Trigger phrases include "find pharmacy", "pharmacies near", "drugstore in", "retail pharmacy", "specialty pharmacy"
version: 1.0.0
status: active
product: networksim-local
related_skills:
  - provider-lookup
  - geographic-search
  - facility-lookup
---

# Pharmacy Lookup

Find pharmacies by location or type.

## Overview

Search the NPPES registry for pharmacies:
- Community/Retail Pharmacies
- Mail Order Pharmacies
- Specialty Pharmacies
- Compounding Pharmacies
- Hospital/Institutional Pharmacies
- Long Term Care Pharmacies

## Trigger Phrases

- "Find pharmacies in [location]"
- "Pharmacy near ZIP [code]"
- "Retail pharmacies in [city]"
- "Specialty pharmacy in [state]"
- "Find a drugstore near [location]"

## Parameters

| Parameter | Required | Type | Description |
|-----------|----------|------|-------------|
| pharmacy_type | Optional | String | Type of pharmacy |
| state | Conditional | String | 2-letter state code |
| city | Optional | String | City name |
| zip | Conditional | String | ZIP code |

## Pharmacy Types (Taxonomy Codes)

| Pharmacy Type | Taxonomy Code | Description |
|---------------|---------------|-------------|
| Community/Retail | 3336C0003X | CVS, Walgreens, etc. |
| Mail Order | 3336M0002X | Mail-order pharmacies |
| Specialty | 3336S0011X | Specialty medications |
| Compounding | 3336C0004X | Custom compounding |
| Institutional | 3336I0012X | Hospital pharmacies |
| Long Term Care | 3336L0003X | Nursing home pharmacies |
| Nuclear | 3336N0007X | Nuclear medicine |
| Home Infusion | 3336H0001X | IV therapy at home |
| Clinic | 3336C0002X | Clinic-based |

## Query Patterns

### Pharmacies by Location

```sql
SELECT npi, organization_name, taxonomy_code,
       practice_address_1, practice_city, practice_zip, practice_phone
FROM providers 
WHERE taxonomy_code LIKE '3336%'
  AND practice_city ILIKE 'Boston'
  AND practice_state = 'MA'
ORDER BY organization_name;
```

### Pharmacies by ZIP

```sql
SELECT npi, organization_name, taxonomy_code,
       practice_address_1, practice_city, practice_phone
FROM providers 
WHERE taxonomy_code LIKE '3336%'
  AND practice_zip LIKE '90210%'
ORDER BY organization_name;
```

### Specific Pharmacy Type

```sql
-- Specialty pharmacies in state
SELECT npi, organization_name,
       practice_address_1, practice_city, practice_zip, practice_phone
FROM providers 
WHERE taxonomy_code = '3336S0011X'
  AND practice_state = 'CA'
ORDER BY practice_city;
```

## Examples

### Example 1: Retail Pharmacies

**User**: Find pharmacies near ZIP 10001

**Response**:
```
Found 89 pharmacies near ZIP 10001 (Manhattan, NY)

Community/Retail Pharmacies:
1. CVS Pharmacy #2156 - NPI: 1234567890
   350 5th Ave, New York, NY 10001
   (212) 555-1234

2. Walgreens #3421 - NPI: 2345678901
   460 Park Ave S, New York, NY 10016
   (212) 555-5678

3. Duane Reade #14234 - NPI: 3456789012
   100 W 33rd St, New York, NY 10001
   (212) 555-9012

Specialty Pharmacies:
1. CVS Specialty - NPI: 4567890123
   485 Madison Ave, New York, NY 10022
   (877) 555-1234

Source: NPPES Registry, December 2024
```

### Example 2: Specialty Pharmacies

**User**: Find specialty pharmacies in Florida

**Response**:
```
Found 234 specialty pharmacies (3336S0011X) in Florida

Top Cities:
  Miami: 67
  Orlando: 45
  Tampa: 34
  Jacksonville: 23

Sample Facilities:
1. Accredo Health - NPI: 1122334455
   Specialty Pharmacy | 1640 Century Center Pkwy, Memphis
   (serving FL via mail)

2. CVS Specialty - NPI: 2233445566
   Specialty Pharmacy | 2211 Sanders Rd, Northbrook
   (serving FL via mail)

3. Biologics By McKesson - NPI: 3344556677
   Specialty Pharmacy | 6555 State Hwy 161, Irving
   (serving FL via mail)

Note: Many specialty pharmacies operate via mail order

Source: NPPES Registry, December 2024
```

### Example 3: Compounding Pharmacies

**User**: Compounding pharmacies in Los Angeles

**Response**:
```
Found 45 compounding pharmacies (3336C0004X) in Los Angeles, CA

Sample Facilities:
1. University Compounding Pharmacy - NPI: 1234567890
   1875 S Bascom Ave, San Jose, CA 95128
   (408) 555-1234

2. Professional Arts Pharmacy - NPI: 2345678901
   8111 Beverly Blvd, Los Angeles, CA 90048
   (323) 555-5678

3. College Pharmacy - NPI: 3456789012
   3505 Austin Bluffs Pkwy, Colorado Springs, CO
   (800) 555-9012 (mail order to CA)

Source: NPPES Registry, December 2024
```

## Pharmacy Distribution by State

```sql
-- Count pharmacies by state
SELECT practice_state, COUNT(*) as pharmacy_count
FROM providers
WHERE taxonomy_code LIKE '3336%'
GROUP BY practice_state
ORDER BY pharmacy_count DESC
LIMIT 10;
```

## Cross-Product Integration

**RxMemberSim**: Use for realistic pharmacy NPIs in prescription claims
```sql
-- Random retail pharmacy for claim
SELECT npi, organization_name, practice_city, practice_state, practice_zip
FROM providers 
WHERE taxonomy_code = '3336C0003X'  -- Retail
  AND practice_zip LIKE ? || '%'
ORDER BY RANDOM() 
LIMIT 1;
```

**MemberSim**: Use for pharmacy network validation
```sql
-- Pharmacies in member's ZIP area
SELECT npi, organization_name, practice_address_1, practice_phone
FROM providers 
WHERE taxonomy_code LIKE '3336%'
  AND practice_zip LIKE ? || '%'
LIMIT 10;
```

## Validation Rules

1. Pharmacy searches filter by taxonomy prefix `3336`
2. Only Type 2 (Organization) entities included
3. Results ordered by organization name
4. Only active pharmacies returned

## Notes

- NCPDP Provider IDs are not available in NPPES
- Pharmacy chains may have multiple NPIs (one per location)
- Mail order pharmacies may show corporate HQ address
- Some specialty pharmacies serve multiple states via mail

## Related Skills

- [Provider Lookup](provider-lookup.md) - Look up by NPI
- [Geographic Search](geographic-search.md) - Find by location
- [Facility Lookup](facility-lookup.md) - Find hospitals/facilities
