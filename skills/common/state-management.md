---
name: state-management
description: "Save, load, and manage workspace scenarios to preserve synthetic data across sessions. Auto-persist for token-efficient batch operations. Query saved data with SQL. Triggers: save, load, scenario, persist, resume, continue, list scenarios, delete scenario, export scenario, import scenario, share scenario, query scenario, get summary"
---

# State Management

_Save, load, and manage workspace scenarios to preserve your synthetic healthcare data across sessions. Use auto-persist for token-efficient batch operations._

## For Claude

Use this skill when the user wants to persist their work or resume from a previous session. This skill teaches you how to manage scenarios - named snapshots of the workspace containing all generated entities (patients, encounters, claims, etc.) with full provenance tracking.

**Two Persistence Patterns**:

1. **Traditional Save/Load** - Full data in context. Use for small scenarios (<50 entities) or when the user needs all data immediately.

2. **Auto-Persist Pattern** (Recommended for large batches) - Token-efficient persistence. Returns summary (~500 tokens) instead of echoing back all data. Use for:
   - Generating 50+ entities
   - Batch operations
   - When you need to persist without filling context

You should apply this knowledge when:
- The user asks to save their current work ("save this", "let's save my progress")
- The user wants to resume from a previous session ("load my scenario", "continue from yesterday")
- The user wants to see what scenarios they have saved ("what scenarios do I have?")
- The user wants to clean up old scenarios ("delete the test scenario")
- The user wants to share a scenario ("export for sharing", "send to colleague")
- The user receives a scenario file ("import this scenario")
- **After generating large batches**, use auto-persist to avoid context overflow
- **When querying specific data** from a saved scenario

## Purpose

State Management enables users to capture their entire workspace as a named scenario that can be restored later. This is essential for:

- **Session continuity** - Save work at the end of a session, resume later
- **Scenario libraries** - Build collections of reusable cohorts
- **Reproducibility** - Share exact configurations with colleagues
- **Experimentation** - Save before making major changes, restore if needed
- **Token efficiency** - Generate large batches without filling context

A scenario captures:
- All entities (patients, encounters, diagnoses, labs, vitals, medications, claims, etc.)
- Complete provenance for every entity (how it was created)
- User-provided metadata (name, description, tags)

## Trigger Phrases

### Traditional Save/Load
- "Save this scenario as..."
- "Save my patients as..."
- "Load scenario..."
- "Open the [name] scenario"

### Auto-Persist (Token-Efficient)
- "Generate 100 patients and save them"
- "Persist these entities"
- "Save without showing all the data"
- "Get a summary of [scenario]"
- "Query the [scenario] for..."
- "Show me patients where..."

### Management
- "List my scenarios"
- "Show available scenarios"
- "Delete scenario..."
- "Rename scenario..."
- "Export [scenario] as JSON"
- "Import scenario from [path]"
- "Tag this scenario with..."
- "Find scenarios tagged..."

## Domain Knowledge

### What is a Scenario?

A scenario is a complete snapshot of the workspace. It includes:

1. **Metadata** - Name, description, tags, timestamps
2. **All Entities** - Patients, encounters, diagnoses, labs, vitals, medications, procedures, notes, members, claims, prescriptions, subjects, trial visits
3. **Provenance** - How each entity was created

### Two Persistence Patterns

#### Pattern 1: Traditional Save/Load (Full Data)

Best for:
- Small scenarios (< 50 entities)
- When user needs immediate access to all data
- Interactive exploration

```python
# Save - returns scenario ID
scenario_id = save_scenario('my-cohort', {'patients': [...]})

# Load - returns ALL entities (can be large!)
scenario = load_scenario('my-cohort')
patients = scenario['entities']['patients']  # Full data in context
```

#### Pattern 2: Auto-Persist (Token-Efficient) ⭐ RECOMMENDED

Best for:
- Large batches (50+ entities)
- Batch generation workflows
- Avoiding context overflow

```python
# Persist - returns summary (~500 tokens), not full data
result = persist(
    {'patients': patient_list, 'encounters': encounter_list},
    context='diabetes cohort San Diego'  # Used for auto-naming
)
# result.scenario_name: "diabetes-cohort-20241227"
# result.summary: ScenarioSummary with counts and statistics

# Get summary - load metadata without full data (~500 tokens)
summary = get_summary('diabetes-cohort-20241227')
# summary.entity_counts: {'patients': 100, 'encounters': 250}
# summary.statistics: {'age_range': [35, 78], 'gender_distribution': {...}}

# Query specific data with pagination
results = query_scenario(
    'diabetes-cohort-20241227',
    "SELECT given_name, family_name, birth_date FROM patients WHERE gender = 'F'",
    limit=20
)
# Only returns the 20 rows you asked for
```

### Auto-Naming

When using `persist()`, if no explicit name is provided, the system automatically generates a descriptive name:

- Extracts healthcare-relevant keywords from context
- Adds date stamp for uniqueness
- Format: `{keywords}-{YYYYMMDD}`

Examples:
- Context: "diabetes patients in San Diego" → `diabetes-patients-20241227`
- Context: "Medicare members over 65" → `medicare-members-20241227`
- Context: "Phase 3 oncology trial" → `oncology-trial-20241227`

### Scenario Storage

Scenarios are stored in a DuckDB database at `~/.healthsim/healthsim.duckdb`. This provides:
- Fast save and load operations
- Efficient storage with compression
- SQL query capability for advanced users
- Scenario-scoped queries via `scenario_id` column

For sharing scenarios between users, export to JSON format.

## Generation Guidelines

### Auto-Persist Pattern (Recommended for Large Batches)

**When generating 50+ entities**, use auto-persist to avoid filling context:

**Example - Generate 100 Medicare Members**:
```
User: Generate 100 Medicare members over 65 in California

Claude: [Generates members using MemberSim skill]
        [Persists using auto-persist]

Saved "medicare-members-20241227":
- 100 members persisted
- Age range: 65-89
- Geographic: California

Use "query medicare-members-20241227" to explore specific subsets.
```

**Example - Query Saved Data**:
```
User: Show me female members from that cohort

Claude: [Queries scenario with SQL]

Found 48 female members:

| Given Name | Family Name | Birth Date | City |
|------------|-------------|------------|------|
| Margaret   | Wilson      | 1952-03-15 | LA   |
| Dorothy    | Chen        | 1948-11-22 | SF   |
...

Showing 20 of 48 results. Say "show more" for next page.
```

### Traditional Save/Load (For Small Scenarios)

**When the user says**: "Save my patients" (with < 50 entities)

**Claude should**:
1. Ask for a name if not provided
2. Optionally ask for description and tags
3. Call save_scenario with appropriate parameters
4. Confirm what was saved with summary statistics

**Example**:
```
User: Save this as diabetes-cohort

Claude: [Saves to database]

Saved "diabetes-cohort":
- 15 patients with full clinical data
- 47 encounters, 182 lab results
- Tags: (none)

You can load this anytime with "load diabetes-cohort".
```

### Loading a Scenario

**Two options based on need**:

1. **Load Summary Only** (token-efficient):
```
User: What's in my diabetes scenario?

Claude: [Calls get_summary]

"diabetes-cohort" summary:
- 15 patients (8 male, 7 female)
- Age range: 45-72 years
- 47 encounters, 182 labs
- Top conditions: E11.9 (Type 2 DM), I10 (Hypertension)

Need specific data? I can query for particular patients or conditions.
```

2. **Load Full Data** (when needed):
```
User: Load all my diabetes patients - I need to review each one

Claude: [Calls load_scenario - full data in context]

Loaded "diabetes-cohort" with 15 patients:
[Full patient details...]
```

### Querying Scenarios

**When the user wants specific data from a saved scenario**:

**Claude should**:
1. Identify the scenario to query
2. Construct appropriate SQL (SELECT only)
3. Call query_scenario with pagination
4. Present results in a readable format

**Example**:
```
User: Show me patients with A1C > 9 from my diabetes cohort

Claude: [Queries scenario]

Found 4 patients with A1C > 9.0:

| Name | A1C | Last Visit |
|------|-----|------------|
| John Smith | 9.8 | 2024-01-15 |
| Maria Garcia | 10.2 | 2024-02-20 |
| Robert Lee | 9.3 | 2024-03-01 |
| Susan Brown | 11.1 | 2024-01-28 |

These patients may need medication adjustment.
```

### Listing Scenarios

**When the user says**: "What scenarios do I have?"

**Claude should**:
1. Call list_scenarios with any search/filter criteria
2. Present results in a scannable format
3. Offer to load summary or query specific ones

### Deleting a Scenario

**When the user says**: "Delete the test scenario"

**Claude should**:
1. Identify the scenario to delete
2. **Always confirm before deleting** (deletion requires confirm=True)
3. Call delete_scenario with confirm=True
4. Confirm deletion

**Example**:
```
User: Delete test-patients

Claude: Are you sure you want to delete "test-patients"?
This contained 3 patients and cannot be undone.

User: Yes

Claude: [Deletes with confirm=True]

Deleted "test-patients". You have 3 remaining scenarios.
```

### Proactive Auto-Persist

**When to automatically persist**:
- After generating 50+ entities: Auto-persist, show summary
- After batch generation completes: "Persisted 100 members as 'medicare-batch-20241227'"
- When context is filling up: Persist and continue with summary

## Examples

### Example 1: Auto-Persist Batch Generation

```
User: Generate 200 patients with various chronic conditions

Claude: [Generates patients in batches]
        [Auto-persists to avoid context overflow]

Generated and saved "chronic-conditions-20241227":
- 200 patients persisted
- Conditions: Diabetes (45), Hypertension (78), COPD (32), CHF (25), Other (20)
- Age range: 35-85

The full data is saved. Would you like to:
- Query specific conditions ("show COPD patients")
- Get samples ("show me 3 example patients")
- Export for analysis
```

### Example 2: Query Workflow

```
User: From my chronic conditions scenario, show diabetes patients over 60

Claude: [Queries scenario with SQL]

Found 28 diabetes patients over 60:

| Name | Age | A1C | Comorbidities |
|------|-----|-----|---------------|
| James Wilson | 67 | 7.8 | HTN, CKD |
| Patricia Lee | 72 | 8.2 | HTN |
...

Showing 20 of 28. Say "next page" for more.
```

### Example 3: Get Samples Without Full Load

```
User: Show me a few example patients from the scenario

Claude: [Gets samples with diverse strategy]

Here are 3 representative patients:

1. **John Smith** (Male, 58)
   - Conditions: Type 2 DM, Hypertension
   - Recent A1C: 7.4

2. **Maria Garcia** (Female, 71)
   - Conditions: COPD, CHF
   - Last Visit: 2024-02-15

3. **Robert Chen** (Male, 45)
   - Conditions: Type 2 DM
   - Recent A1C: 8.1

Want to see more samples or query for specific criteria?
```

### Example 4: Resume Work on Large Cohort

```
User: Continue working on my medicare scenario from yesterday

Claude: [Gets summary - doesn't load all data]

Loaded summary for "medicare-members-20241227":
- 500 members
- Geographic: California, Texas, Florida
- Age range: 65-92
- Last updated: yesterday at 3:45 PM

What would you like to do?
- Generate more members
- Query specific subsets
- Export for analysis
```

## Parameters

### persist()
| Parameter | Description | Type | Default |
|-----------|-------------|------|---------|
| entities | Dict of entity type → list | dict | (required) |
| context | Context for auto-naming | string | (optional) |
| scenario_name | Explicit name | string | (auto-generated) |
| tags | Organization keywords | string[] | (optional) |

### get_summary()
| Parameter | Description | Type | Default |
|-----------|-------------|------|---------|
| scenario_id_or_name | Scenario identifier | string | (required) |
| include_samples | Include sample entities | boolean | true |
| samples_per_type | Samples per entity type | int | 3 |

### query_scenario()
| Parameter | Description | Type | Default |
|-----------|-------------|------|---------|
| scenario_id_or_name | Scenario identifier | string | (required) |
| sql | SELECT query | string | (required) |
| limit | Max results | int | 20 |
| offset | Pagination offset | int | 0 |

### save_scenario() (Traditional)
| Parameter | Description | Type | Default |
|-----------|-------------|------|---------|
| name | Scenario identifier | string | (required) |
| entities | Dict of entity type → list | dict | (required) |
| description | Notes about contents | string | (optional) |
| tags | Organization keywords | string[] | (optional) |
| overwrite | Replace existing | boolean | false |

## Related Skills

- [PatientSim](../patientsim/SKILL.md) - Generate patient data
- [MemberSim](../membersim/SKILL.md) - Generate member/claims data
- [RxMemberSim](../rxmembersim/SKILL.md) - Generate pharmacy data
- [TrialSim](../trialsim/SKILL.md) - Generate clinical trial data
- [DuckDB Skill](./duckdb-skill.md) - Advanced database queries

## Metadata

- **Type**: domain-knowledge
- **Version**: 3.0
- **Format**: Claude-Optimized (v2.0)
- **Author**: HealthSim Team
- **Tags**: state-management, persistence, scenarios, export, import, auto-persist, query
- **Created**: 2025-01-26
- **Updated**: 2025-12-27
