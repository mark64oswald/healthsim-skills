# State Management

_Save, load, and manage workspace scenarios to preserve your synthetic patient data across sessions._

## For Claude

Use this skill when the user wants to persist their work or resume from a previous session. This skill teaches you how to manage scenarios - named snapshots of the workspace that contain all patients and their clinical data with full provenance tracking.

You should apply this knowledge when:
- The user asks to save their current work ("save this", "let's save my progress")
- The user wants to resume from a previous session ("load my scenario", "continue from yesterday")
- The user wants to see what scenarios they have saved ("what scenarios do I have?")
- The user wants to clean up old scenarios ("delete the test scenario")
- After significant work, proactively suggest saving

This skill provides guidance on workspace persistence, scenario organization, and managing the save/load lifecycle.

## Purpose

State Management enables users to capture their entire workspace as a named scenario that can be restored later. This is essential for:

- **Session continuity** - Save work at the end of a session, resume later
- **Scenario libraries** - Build collections of reusable patient cohorts
- **Reproducibility** - Share exact patient configurations with colleagues
- **Experimentation** - Save before making major changes, restore if needed

A scenario captures:
- All patients and their demographics
- All clinical data (encounters, diagnoses, labs, vitals, medications)
- Complete provenance for every entity (how it was created)
- User-provided metadata (name, description, tags)

## When to Use This Skill

Apply this skill when the user mentions:

**Direct Keywords**:
- "save", "export", "persist", "store", "backup"
- "load", "restore", "open", "resume", "continue"
- "scenario", "snapshot", "workspace", "session"
- "list scenarios", "show saved", "what did I save"

**Implicit Indicators**:
- Finishing a session ("I'm done for today", "let's wrap up")
- About to make major changes ("before we change everything...")
- Starting fresh ("start from where we left off")
- Cleaning up ("delete the old ones")

**Proactive Triggers** - Suggest saving when:
- User has generated a significant cohort (10+ patients)
- User has spent time customizing patient data
- User says they're finished or switching tasks
- User is about to clear the workspace or start over

## Domain Knowledge

### What is a Scenario?

A scenario is a complete snapshot of the workspace at a point in time. It includes:

1. **Metadata** - Name, description, tags, timestamps
2. **Provenance Summary** - Statistics about how data was created
3. **All Entities** - Patients, encounters, diagnoses, labs, vitals, medications, procedures, notes

Each entity retains its provenance information:
- `source_type`: How it was created (`loaded`, `generated`, `derived`)
- `source_system`: Where data originated (e.g., "patientsim", "user-input", "csv-import")
- `skill_used`: Which skill guided generation (e.g., "diabetes-management")
- `created_at`: When the entity was created

**Why provenance matters**: When you load a scenario, you know exactly how each piece of data was created. A loaded patient that was originally generated with the "sepsis-acute-care" skill retains that information.

### Scenario Storage

Scenarios are stored as JSON files in `~/.healthsim/scenarios/`:
```
~/.healthsim/
  scenarios/
    diabetes-training-cohort.json
    ed-simulation-2024-01.json
    my-test-patients.json
```

Each file is a self-contained JSON document that can be:
- Backed up and shared
- Version controlled
- Inspected with standard tools

### Workspace Scopes

When saving or loading, you can specify scope:

**Full Workspace (default)**:
- Saves/loads everything in the current session
- Use when you want a complete snapshot

**Selected Patients**:
- Save/load specific patients by ID or MRN
- Use when you want to extract a subset
- Useful for combining patients from multiple scenarios

### Load Modes

When loading a scenario:

**Replace Mode (default)**:
- Clears the current workspace
- Loads only the scenario contents
- Use when starting fresh from a saved state

**Merge Mode**:
- Keeps existing workspace contents
- Adds scenario contents to workspace
- Resolves conflicts by patient MRN (scenario wins or keeps both)
- Use when combining cohorts

### Naming Scenarios

Good scenario names are:
- Descriptive: "diabetes-progression-cohort" not "test1"
- Dated if relevant: "ed-training-2024-q1"
- Consistent: Use kebab-case, avoid spaces

Tags help organize:
- Clinical domain: "diabetes", "cardiology", "oncology"
- Purpose: "training", "testing", "demo"
- Project: "project-alpha", "workshop-materials"

## Generation Guidelines

### Saving a Scenario

**When the user says**: "Save my patients" or "Let's save this as a scenario"

**Claude should**:
1. Ask for a name if not provided
2. Optionally ask for description and tags
3. Determine scope (all patients or specific ones)
4. Call `healthsim.save_scenario` with appropriate parameters
5. Confirm what was saved with summary statistics

**Conversational flow**:
```
User: Save my work

Claude: I'll save your current workspace as a scenario. What would you
like to call it?

User: diabetes-cohort

Claude: Great! Any description or tags to help you find it later?

User: It's for the Q1 training workshop, tag it with "training" and "diabetes"

Claude: [Calls save_scenario]

Perfect! I've saved "diabetes-cohort":
- 15 patients with full clinical data
- 47 encounters, 182 lab results
- Provenance: 12 generated, 3 derived from loaded data
- Tags: training, diabetes

You can load this anytime with "load diabetes-cohort".
```

### Loading a Scenario

**When the user says**: "Load my scenario" or "Continue from yesterday"

**Claude should**:
1. If name not specified, list recent scenarios
2. Confirm the scenario to load (fuzzy match on name)
3. Ask about mode if context suggests merge might be wanted
4. Call `healthsim.load_scenario`
5. Summarize what was loaded

**Conversational flow**:
```
User: Load my diabetes scenario

Claude: I found "diabetes-cohort" saved yesterday. Should I:
- Replace the current workspace (you have 3 patients that will be cleared)
- Merge with your current patients

User: Replace it

Claude: [Calls load_scenario with mode="replace"]

Loaded "diabetes-cohort":
- 15 patients now in your workspace
- Original provenance preserved
- Ready to continue where you left off!

What would you like to work on?
```

### Listing Scenarios

**When the user says**: "What scenarios do I have?" or "Show my saved work"

**Claude should**:
1. Call `healthsim.list_scenarios` with any search/filter criteria
2. Present results in a scannable format
3. Offer to load or get details on specific ones

**Conversational flow**:
```
User: What have I saved?

Claude: [Calls list_scenarios]

Here are your saved scenarios:

Recent:
- diabetes-cohort (yesterday) - 15 patients, tags: training, diabetes
- ed-simulation (3 days ago) - 50 patients, tags: emergency, simulation

Older:
- test-patients (2 weeks ago) - 3 patients
- cardiac-demo (1 month ago) - 8 patients, tags: cardiology, demo

Would you like to load one of these or see more details?
```

### Deleting a Scenario

**When the user says**: "Delete the test scenario" or "Remove old scenarios"

**Claude should**:
1. Identify the scenario(s) to delete
2. **Always confirm before deleting**
3. Call `healthsim.delete_scenario` with confirm=true
4. Confirm deletion

**Conversational flow**:
```
User: Delete test-patients

Claude: Are you sure you want to delete "test-patients"?
This contained 3 patients and cannot be undone.

User: Yes

Claude: [Calls delete_scenario with confirm=true]

Deleted "test-patients". You have 3 remaining scenarios.
```

### Proactive Saving

**When to suggest saving**:
- After generating a large cohort: "You've built up 25 patients - would you like to save this as a scenario?"
- End of significant work: "Before we move on, want me to save your current workspace?"
- Before destructive operations: "This will clear your workspace. Save first?"

**How to suggest**:
- Be helpful, not pushy
- Offer a suggested name based on context
- Make it easy to decline

```
Claude: You've generated 25 diabetes patients with good variety.
Would you like to save this as a scenario before we continue?
I'd suggest "diabetes-cohort-25" or you can name it yourself.
```

## Error Handling

### Scenario Not Found
```
User: Load my cardio scenario

Claude: I couldn't find a scenario matching "cardio".
Here are your saved scenarios:
- diabetes-cohort
- ed-simulation
- cardiac-demo

Did you mean "cardiac-demo"?
```

### Merge Conflicts
```
Claude: Found 2 patients in your workspace that have the same MRN as
patients in "diabetes-cohort":
- MRN12345 (John Smith) - exists in both
- MRN67890 (Jane Doe) - exists in both

How should I handle these?
- Keep workspace version (skip these from scenario)
- Use scenario version (overwrite workspace)
- Keep both (scenario patients get new MRNs)
```

### Empty Workspace on Save
```
Claude: There's nothing in your workspace to save.
Generate some patients first with generate_patient or generate_cohort.
```

## Parameters

Parameters for natural language customization:

| Parameter | Natural Language Description | Type | Default | Claude's Interpretation |
|-----------|------------------------------|------|---------|-------------------------|
| name | "What should we call this scenario?" | string | (required) | Kebab-case identifier for the scenario file |
| description | "Any notes about what this contains?" | string | (optional) | Free text stored in scenario metadata |
| tags | "Any tags to help organize?" | string[] | (optional) | Array of keywords for filtering |
| scope | "All patients or specific ones?" | enum: all, patients | all | Whether to save entire workspace or selected patients |
| mode | "Replace or merge with current?" | enum: replace, merge | replace | How to handle existing workspace when loading |

## Example Requests and Interpretations

### Example 1: Simple Save

**User says**: "Save this as my-test"

**Claude interprets**:
- Name: "my-test"
- No description or tags provided
- Scope: all (default)

**Claude calls**: `healthsim.save_scenario(name="my-test", scope="all")`

### Example 2: Save with Metadata

**User says**: "Save the current patients as 'workshop-demo' for the training session, tag it training and oncology"

**Claude interprets**:
- Name: "workshop-demo"
- Description: "for the training session"
- Tags: ["training", "oncology"]
- Scope: all

**Claude calls**: `healthsim.save_scenario(name="workshop-demo", description="for the training session", tags=["training", "oncology"], scope="all")`

### Example 3: Load Most Recent

**User says**: "Load my last scenario"

**Claude interprets**:
- User wants most recently saved scenario
- No specific name provided

**Claude calls**: `healthsim.list_scenarios(limit=1)` then `healthsim.load_scenario(scenario_id=<most_recent>)`

### Example 4: Partial Save

**User says**: "Save just the first 3 patients as a test set"

**Claude interprets**:
- Scope: patients
- Patient selection: first 3 in workspace

**Claude calls**: `healthsim.save_scenario(name="test-set", scope="patients", patient_ids=[id1, id2, id3])`

### Example 5: Merge Load

**User says**: "Add the diabetes patients to what I have"

**Claude interprets**:
- Load scenario matching "diabetes"
- Mode: merge (add to existing)

**Claude calls**: `healthsim.load_scenario(name="diabetes-cohort", mode="merge")`

## Related Skills

Complementary skills:

- [SKILL.md](../../SKILL.md) - Core HealthSim routing and overview
- [patientsim/SKILL.md](../patientsim/SKILL.md) - PatientSim clinical scenarios
- [membersim/SKILL.md](../membersim/SKILL.md) - MemberSim claims scenarios

## Related Documentation

- [State Management Specification](../../docs/state-management/specification.md)
- [State Management User Guide](../../docs/state-management/user-guide.md)

## Metadata

- **Type**: domain-knowledge
- **Version**: 1.0
- **Format**: Claude-Optimized (v2.0)
- **Author**: HealthSim Team
- **Tags**: state-management, persistence, scenarios, workspace
- **Created**: 2025-01-26
- **Updated**: 2025-01-26
