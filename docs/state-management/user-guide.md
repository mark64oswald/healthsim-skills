# State Management

**Save your work. Pick up where you left off. Build complex cases over multiple sessions.**

## Overview

A **scenario** is a snapshot of your workspace - all the patients, encounters, claims, and other entities you've generated, with complete information about how each piece was created. Think of it like saving a document: you can close HealthSim, come back tomorrow, and pick up exactly where you left off.

Why save your work?

- **Session continuity** - Work on complex patient cases across multiple sessions
- **Build libraries** - Create reusable cohorts for different testing scenarios
- **Experiment safely** - Save before making major changes; restore if needed
- **Share work** - Export scenarios as JSON files to share with colleagues

## Quick Start

### Save in 10 seconds

After generating some patients, just say:

```text
Save this as my-test-cohort
```

> **Claude:** **Saved "my-test-cohort"**
> - 15 patients with full clinical data
> - 47 encounters, 182 lab results
> - Tags: (none)
>
> You can load this anytime with "load my-test-cohort".

### Load in 10 seconds

To continue where you left off:

```text
Load my-test-cohort
```

> **Claude:** **Loaded "my-test-cohort"**
> - 15 patients now in your workspace
> - All clinical data and history preserved
>
> Ready to continue! What would you like to work on?

That's it! Read on for more options and details.

---

## Saving Scenarios

### Basic Save

The simplest way to save - just give it a name:

```text
Save my work as diabetes-cohort
```

Claude will save everything in your current workspace and confirm what was captured.

### Save with Description and Tags

Add context to help you find and organize scenarios later:

```text
Save this as workshop-demo for the Q1 training session, tag it training and diabetes
```

> **Claude:** **Saved "workshop-demo"**
> - 25 patients with full clinical data
> - Description: "for the Q1 training session"
> - Tags: training, diabetes
>
> This scenario is ready for your workshop!

### Overwriting Scenarios

To update an existing scenario with the same name:

```text
Save this as diabetes-cohort and overwrite if it exists
```

> **Claude:** **Updated "diabetes-cohort"**
> - Previous version replaced
> - 30 patients (was 25)

**Tip:** Claude will suggest saving after significant work. If you've built up a good cohort, you might see: "You've generated 30 patients with detailed clinical data. Would you like to save this as a scenario before we continue?"

---

## Loading Scenarios

### Load by Name

Just ask for the scenario you want:

```text
Load my diabetes-cohort
```

Claude uses fuzzy matching, so you don't need the exact name. "Load diabetes" would find "diabetes-cohort" too.

### Load Most Recent

Can't remember the name? Just ask for your last work:

```text
Load my last scenario
```

> **Claude:** I found "workshop-demo" saved 2 hours ago. Loading now...
>
> **Loaded "workshop-demo"**
> - 25 patients now in your workspace
> - All clinical data preserved

### Browse and Choose

Not sure what you have? Ask to see your options:

```text
What scenarios do I have?
```

> **Claude:** **Your saved scenarios:**
>
> **Recent:**
> - **workshop-demo** (2 hours ago) - 25 patients, tags: training, diabetes
> - **ed-simulation** (yesterday) - 50 patients, tags: emergency
>
> **Older:**
> - **cardiac-demo** (1 week ago) - 8 patients, tags: cardiology
> - **test-patients** (2 weeks ago) - 3 patients
>
> Would you like to load one of these?

```text
Load the ED one
```

> **Claude:** **Loaded "ed-simulation"** - 50 patients now in your workspace.

---

## Managing Your Scenarios

### Search and Filter

Find scenarios by tags or keywords:

```text
Show me scenarios tagged with training
```

```text
Find scenarios with diabetes patients
```

### Delete Scenarios

Clean up scenarios you no longer need:

```text
Delete the test-patients scenario
```

> **Claude:** Are you sure you want to delete "test-patients"?
> This contained 3 patients and **cannot be undone**.

```text
Yes, delete it
```

> **Claude:** **Deleted "test-patients"**
> You have 3 remaining scenarios.

**Note:** Claude will always ask for confirmation before deleting. Deleted scenarios cannot be recovered.

---

## Sharing Scenarios

### Export to JSON

To share a scenario with a colleague, export it as a JSON file:

```text
Export my diabetes-cohort
```

> **Claude:** **Exported "diabetes-cohort"**
> - Saved to: ~/Downloads/diabetes-cohort.json
> - 25 patients, 150 entities total
>
> Share this file with your colleagues!

### Import from JSON

When you receive a scenario file:

```text
Import the scenario from ~/Downloads/shared-scenario.json
```

> **Claude:** **Imported "shared-scenario"**
> - 50 patients added to your scenarios
> - Ready to load with "load shared-scenario"

You can also override the name:

```text
Import ~/Downloads/data.json as my-imported-cohort
```

---

## Understanding What's Saved

### What's Included

When you save a scenario, you get a complete snapshot:

**Everything in Your Workspace:**
- **Patients** - Demographics, identifiers, contact info
- **Encounters** - Visits, admissions, ED presentations
- **Diagnoses** - All conditions with ICD-10 codes
- **Medications** - Current and historical medications
- **Lab Results** - All labs with values and reference ranges
- **Vital Signs** - Temperature, BP, heart rate, etc.
- **Procedures** - Surgeries and other procedures
- **Clinical Notes** - Any generated documentation
- **Members/Claims** - Health plan data (if generated)
- **Prescriptions** - Pharmacy data (if generated)
- **Subjects/Visits** - Clinical trial data (if generated)

### Provenance: Knowing Where Data Came From

Every piece of data in a scenario includes **provenance** - information about how it was created. This is preserved exactly when you save and load.

Provenance tells you:

| Field | What it means | Example |
|-------|---------------|---------|
| `source_type` | How the data was created | `generated`, `loaded`, `derived` |
| `source_system` | What system created it | `patientsim`, `membersim` |
| `skill_used` | Which clinical skill guided generation | `diabetes-management` |

**Why this matters:** When you load a scenario, you know exactly what's synthetic vs what came from other sources. A patient generated with the "sepsis-acute-care" skill keeps that information.

### What's NOT Saved

- **Conversation history** - Your chat with Claude is separate from scenarios
- **Export files** - FHIR/HL7 exports are separate operations
- **Validation results** - These are regenerated when needed

---

## Practical Examples

### Example 1: Building a Complex Case Over Multiple Sessions

You're creating a complex diabetic patient for testing. This takes multiple sessions:

**Session 1: Create the base patient**

```text
Generate a 65-year-old diabetic patient with 10 years of disease history
```

> **Claude:** Generated Robert Chen, 65-year-old male with Type 2 Diabetes...

```text
Add retinopathy that developed 3 years ago
```

> **Claude:** Added diabetic retinopathy (E11.319) diagnosed in 2022...

```text
Save this as complex-diabetes-case
```

> **Claude:** **Saved "complex-diabetes-case"** - 1 patient with detailed clinical history.

**Session 2: Continue building (next day)**

```text
Load my complex diabetes case
```

> **Claude:** **Loaded "complex-diabetes-case"** - Robert Chen is in your workspace.

```text
Add nephropathy and update his medications accordingly
```

> **Claude:** Added diabetic nephropathy (E11.21), updated medications:
> - Added ACE inhibitor for renal protection
> - Adjusted metformin dose for eGFR 45

```text
Save this - same name and overwrite
```

> **Claude:** **Updated "complex-diabetes-case"** with your latest changes.

### Example 2: Creating Variations from a Base

You have a good base cohort and want to create variations for different test cases:

```text
Load my ed-simulation scenario
```

> **Claude:** **Loaded "ed-simulation"** - 50 ED patients.

```text
Increase the severity - make 20 of these patients critically ill
```

> **Claude:** Updated 20 patients with critical presentations...

```text
Save this as ed-simulation-critical
```

> **Claude:** **Saved "ed-simulation-critical"** - 50 patients (20 critical).

Now you have two scenarios: the original and the critical variation. Both are available anytime.

### Example 3: Sharing Work with a Colleague

You've created a useful cohort and want to share it:

```text
Export my integration-test-cohort for sharing
```

> **Claude:** **Exported to ~/Downloads/integration-test-cohort.json**
> - 43 patients across 3 clinical domains
> - Send this file to your colleague!

Your colleague imports it:

```text
Import ~/Downloads/integration-test-cohort.json
```

> **Claude:** **Imported "integration-test-cohort"** - 43 patients ready to use.

---

## Tips and Best Practices

### Naming Conventions

Good scenario names are:
- **Descriptive** - `diabetes-progression-cohort` not `test1`
- **Dated if relevant** - `ed-training-2025-q1`
- **Consistent** - Use kebab-case, avoid spaces

### When to Save

**Save early, save often:**
- After generating a significant cohort (10+ patients)
- Before making major changes to existing patients
- At the end of each work session
- Before clearing your workspace to start something new

### Using Tags Effectively

Tags help you organize and find scenarios. Good tagging strategies:

| Tag type | Examples |
|----------|----------|
| Clinical domain | `diabetes`, `cardiology`, `oncology`, `emergency` |
| Purpose | `training`, `testing`, `demo`, `production` |
| Project | `project-alpha`, `sprint-12`, `workshop-materials` |
| Status | `draft`, `reviewed`, `final` |

### Storage and Portability

Scenarios are stored in a DuckDB database at `~/.healthsim/healthsim.duckdb`. This means:

- **They persist** - Scenarios survive between HealthSim sessions
- **Fast access** - DuckDB provides fast queries even with large datasets
- **Queryable** - Advanced users can query scenarios directly with SQL

**Sharing scenarios:** Use the export/import feature to share scenarios as JSON files. This is the recommended way to share work with colleagues.

### Migrating from JSON Files

If you have existing scenarios stored as JSON files in `~/.healthsim/scenarios/` from an earlier version of HealthSim, you can migrate them:

```bash
python scripts/migrate_json_to_duckdb.py
```

This creates a backup and imports all scenarios to the new DuckDB format.

---

## Related Topics

- [State Management Specification](specification.md) - Technical details for developers
- [Data Architecture](../data-architecture.md) - Database schema and storage details
