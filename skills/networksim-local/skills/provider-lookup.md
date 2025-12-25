---
name: Provider Lookup
description: Look up provider details by NPI number or search by name. Trigger phrases include "lookup NPI", "find provider", "search provider by name", "who is NPI"
version: 1.0.0
status: active
product: networksim-local
related_skills:
  - geographic-search
  - specialty-search
  - facility-lookup
---

# Provider Lookup

Look up real provider information from the NPPES NPI Registry.

## Overview

This skill retrieves actual provider data including:
- Provider name (individual or organization)
- NPI (National Provider Identifier)
- Credentials (MD, DO, NP, PA, etc.)
- Primary specialty (taxonomy code)
- Practice location and contact info

## Trigger Phrases

- "Look up NPI [number]"
- "Find provider with NPI [number]"
- "Who is NPI [number]?"
- "Search for provider [name]"
- "Find Dr. [name]"

## Parameters

| Parameter | Required | Type | Description |
|-----------|----------|------|-------------|
| npi | Conditional | String | 10-digit NPI number |
| name | Conditional | String | Provider or organization name |
| entity_type | Optional | String | 'individual' or 'organization' |

*Either `npi` or `name` is required*

## Query Patterns

### By NPI (Exact Lookup)

```sql
SELECT 
    npi,
    entity_type_code,
    COALESCE(organization_name, last_name || ', ' || first_name) as provider_name,
    credential,
    taxonomy_code,
    practice_address_1,
    practice_city,
    practice_state,
    practice_zip,
    practice_phone
FROM providers 
WHERE npi = '1234567890';
```

### By Name (Search)

```sql
-- Individual providers
SELECT npi, last_name, first_name, credential, taxonomy_code, practice_city, practice_state
FROM providers 
WHERE entity_type_code = '1'
  AND last_name ILIKE 'Smith%'
LIMIT 25;

-- Organizations
SELECT npi, organization_name, taxonomy_code, practice_city, practice_state
FROM providers 
WHERE entity_type_code = '2'
  AND organization_name ILIKE '%Memorial%'
LIMIT 25;
```

## Examples

### Example 1: NPI Lookup

**User**: Look up NPI 1841297959

**Response**:
```
Provider: Franklin Banker
NPI: 1841297959
Entity Type: Individual
Credentials: [from database]
Specialty: [taxonomy code and description]
Practice Location:
  [Address]
  Cameron Park, CA [ZIP]
Phone: [phone number]

Source: NPPES Registry, December 2024
```

### Example 2: Name Search

**User**: Find Dr. Smith in California

**Response**:
```
Found 847 providers matching "Smith" in CA:

1. Smith, John MD - NPI: 1234567890
   Internal Medicine | Los Angeles, CA

2. Smith, Jane DO - NPI: 2345678901
   Family Medicine | San Diego, CA

3. Smith, Robert MD - NPI: 3456789012
   Cardiology | San Francisco, CA

[... additional results]

Source: NPPES Registry, December 2024
```

## Validation Rules

1. NPI must be exactly 10 digits
2. NPI must pass Luhn check algorithm
3. Results limited to active providers (no deactivation date)
4. Name searches return max 50 results

## Response Format

All responses include:
- Provider identification (NPI, name, credentials)
- Practice location
- Primary specialty
- **Source attribution**: "NPPES Registry, [Month Year]"

## Related Skills

- [Geographic Search](geographic-search.md) - Find providers by location
- [Specialty Search](specialty-search.md) - Find providers by specialty
- [Facility Lookup](facility-lookup.md) - Find hospitals and facilities
- [Pharmacy Lookup](pharmacy-lookup.md) - Find pharmacies

## Notes

- Data is from NPPES NPI Registry (public CMS data)
- Updated monthly
- Only active providers are returned
- Foreign providers excluded (US locations only)
