---
name: state-management
description: "Save, load, and manage workspace scenarios to preserve synthetic data across sessions. Export to JSON for sharing. Triggers: save, load, scenario, persist, resume, continue, list scenarios, delete scenario, export scenario, import scenario, share scenario"
---

# State Management

_Save, load, and manage workspace scenarios to preserve your synthetic healthcare data across sessions._

## For Claude

Use this skill when the user wants to persist their work or resume from a previous session. This skill teaches you how to manage scenarios - named snapshots of the workspace containing all generated entities (patients, encounters, claims, etc.) with full provenance tracking.

You should apply this knowledge when:
- The user asks to save their current work ("save this", "let's save my progress")
- The user wants to resume from a previous session ("load my scenario", "continue from yesterday")
- The user wants to see what scenarios they have saved ("what scenarios do I have?")
- The user wants to clean up old scenarios ("delete the test scenario")
- The user wants to share a scenario ("export for sharing", "send to colleague")
- The user receives a scenario file ("import this scenario")
- After significant work, proactively suggest saving

## Purpose

State Management enables users to capture their entire workspace as a named scenario that can be restored later. This is essential for:

- **Session continuity** - Save work at the end of a session, resume later
- **Scenario libraries** - Build collections of reusable cohorts
- **Reproducibility** - Share exact configurations with colleagues
- **Experimentation** - Save before making major changes, restore if needed

A scenario captures:
- All entities (patients, encounters, diagnoses, labs, vitals, medications, claims, etc.)
- Complete provenance for every entity (how it was created)
- User-provided metadata (name, description, tags)

## Trigger Phrases

- "Save this scenario as..."
- "Save my patients as..."
- "Load scenario..."
- "Open the [name] scenario"
- "List my scenarios"
- "Show available scenarios"
- "Delete scenario..."
- "Export [scenario] as JSON"
- "Import scenario from [path]"
- "Share this scenario with..."
- "Tag this scenario with..."
- "Find scenarios tagged..."

## Domain Knowledge

### What is a Scenario?

A scenario is a complete snapshot of the workspace. It includes:

1. **Metadata** - Name, description, tags, timestamps
2. **All Entities** - Patients, encounters, diagnoses, labs, vitals, medications, procedures, notes, members, claims, prescriptions, subjects, trial visits
3. **Provenance** - How each entity was created

Each entity retains its provenance information:
- `source_type`: How it was created (`loaded`, `generated`, `derived`)
- `source_system`: Where data originated (e.g., "patientsim", "membersim")
- `skill_used`: Which skill guided generation (e.g., "diabetes-management")
- `created_at`: When the entity was created

### Scenario Storage

Scenarios are stored in a DuckDB database at `~/.healthsim/healthsim.duckdb`. This provides:
- Fast save and load operations
- Efficient storage with compression
- SQL query capability for advanced users

For sharing scenarios between users, export to JSON format.

### Sharing Scenarios

**Export to JSON**: Creates a portable file that can be shared
- Default location: `~/Downloads/{scenario-name}.json`
- Contains all entities and metadata
- Self-contained and portable

**Import from JSON**: Loads a shared scenario file
- Reads JSON file and imports to database
- Can override the scenario name
- Option to overwrite existing scenarios

## Generation Guidelines

### Saving a Scenario

**When the user says**: "Save my patients" or "Let's save this"

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

**When the user says**: "Load my scenario" or "Continue from yesterday"

**Claude should**:
1. If name not specified, list recent scenarios
2. Confirm the scenario to load (fuzzy match on name)
3. Call load_scenario
4. Summarize what was loaded

**Example**:
```
User: Load my diabetes scenario

Claude: [Loads from database]

Loaded "diabetes-cohort":
- 15 patients now in your workspace
- Original provenance preserved

What would you like to work on?
```

### Listing Scenarios

**When the user says**: "What scenarios do I have?"

**Claude should**:
1. Call list_scenarios with any search/filter criteria
2. Present results in a scannable format
3. Offer to load or get details on specific ones

**Example**:
```
User: What scenarios do I have?

Claude: [Lists from database]

Your saved scenarios:

Recent:
- diabetes-cohort (yesterday) - 15 patients, tags: training, diabetes
- ed-simulation (3 days ago) - 50 patients, tags: emergency

Older:
- cardiac-demo (1 month ago) - 8 patients, tags: cardiology

Would you like to load one of these?
```

### Exporting for Sharing

**When the user says**: "Export this for sharing" or "Send to colleague"

**Claude should**:
1. Identify which scenario to export
2. Call export_scenario_to_json
3. Confirm the file location

**Example**:
```
User: Export diabetes-cohort so I can share it

Claude: [Exports to JSON]

Exported "diabetes-cohort" to:
~/Downloads/diabetes-cohort.json

Share this file with your colleagues. They can import it with:
"Import scenario from [path]"
```

### Importing a Shared Scenario

**When the user says**: "Import this scenario" or provides a JSON file

**Claude should**:
1. Get the file path
2. Ask if they want to override the name (optional)
3. Call import_scenario_from_json
4. Confirm successful import

**Example**:
```
User: Import the scenario from ~/Downloads/shared-data.json

Claude: [Imports from JSON]

Imported "shared-cohort":
- 25 patients, 100 encounters
- Now available to load

Would you like to load it now?
```

### Deleting a Scenario

**When the user says**: "Delete the test scenario"

**Claude should**:
1. Identify the scenario to delete
2. **Always confirm before deleting**
3. Call delete_scenario
4. Confirm deletion

**Example**:
```
User: Delete test-patients

Claude: Are you sure you want to delete "test-patients"?
This contained 3 patients and cannot be undone.

User: Yes

Claude: [Deletes from database]

Deleted "test-patients". You have 3 remaining scenarios.
```

### Proactive Saving

**When to suggest saving**:
- After generating a large cohort: "You've built up 25 patients - save as a scenario?"
- End of significant work: "Before we move on, want me to save your workspace?"
- Before destructive operations: "This will clear your workspace. Save first?"

## Examples

### Example 1: Complete Save/Load Cycle

```
User: Generate 5 patients with Type 2 Diabetes
Claude: [Generates patients with encounters, diagnoses, medications]

User: Save this as diabetes-test-cohort with tags diabetes, testing
Claude: "Saved 'diabetes-test-cohort' (5 patients, 15 encounters, 5 A1C labs)
         Tagged: diabetes, testing"

[Later session]

User: Load my diabetes testing scenario
Claude: [Loads diabetes-test-cohort]
        "Loaded 'diabetes-test-cohort': 5 patients ready for use."
```

### Example 2: Sharing Between Users

```
User: Export my trial simulation for the research team
Claude: [Exports to JSON]
        "Exported 'trial-simulation' to ~/Downloads/trial-simulation.json
         Share this file with your team."

[Teammate's session]

User: Import the trial scenario from ~/Downloads/trial-simulation.json
Claude: "Imported 'trial-simulation': 200 subjects, 1,500 visits."
```

### Example 3: Search and Filter

```
User: Show me scenarios tagged with training
Claude: [Lists filtered]
        "Found 3 scenarios tagged 'training':
         - workshop-demo (25 patients)
         - diabetes-training (15 patients)
         - ed-basics (10 patients)"
```

## Parameters

| Parameter | Description | Type | Default |
|-----------|-------------|------|---------|
| name | Scenario identifier | string | (required) |
| description | Notes about contents | string | (optional) |
| tags | Organization keywords | string[] | (optional) |
| overwrite | Replace existing | boolean | false |

## Related Skills

- [PatientSim](../patientsim/SKILL.md) - Generate patient data
- [MemberSim](../membersim/SKILL.md) - Generate member/claims data
- [RxMemberSim](../rxmembersim/SKILL.md) - Generate pharmacy data
- [TrialSim](../trialsim/SKILL.md) - Generate clinical trial data

## Related Documentation

- [State Management User Guide](../../docs/state-management/user-guide.md)
- [State Management Specification](../../docs/state-management/specification.md)
- [Data Architecture](../../docs/data-architecture.md)

## Metadata

- **Type**: domain-knowledge
- **Version**: 2.0
- **Format**: Claude-Optimized (v2.0)
- **Author**: HealthSim Team
- **Tags**: state-management, persistence, scenarios, export, import
- **Created**: 2025-01-26
- **Updated**: 2025-12-26
