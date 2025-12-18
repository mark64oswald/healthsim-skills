---
name: trialsim-quickstart
description: "Quick start example for generating a small Phase III clinical trial dataset"
---

# TrialSim Quick Start

Generate synthetic clinical trial data with a simple conversation.

## Try It

**Prompt:** "Generate a Phase III oncology trial with 10 subjects across 2 sites"

## What You Get

Claude generates a complete trial dataset:

- **Study** - Protocol definition with treatment arms
- **Sites** - 2 investigator sites with enrollment
- **Subjects** - 10 randomized subjects with demographics
- **Visits** - Scheduled visits per protocol
- **Adverse Events** - Safety data with severity and causality
- **Disposition** - Completion/discontinuation status

## Sample Output

```json
{
  "study": {
    "study_id": "TRL-ONC-301",
    "phase": "III",
    "indication": "Advanced NSCLC",
    "treatment_arms": [
      {"arm_code": "A", "arm_name": "Drug X 200mg"},
      {"arm_code": "B", "arm_name": "Placebo"}
    ]
  },
  "sites": [
    {"site_id": "001", "city": "Boston", "enrollment": 6},
    {"site_id": "002", "city": "Chicago", "enrollment": 4}
  ],
  "subjects": [
    {
      "subject_id": "TRL-ONC-301-001-001",
      "age": 58,
      "sex": "M",
      "arm": "A",
      "disposition": "COMPLETED"
    }
  ],
  "adverse_events": [
    {
      "subject_id": "TRL-ONC-301-001-001",
      "ae_term": "Fatigue",
      "severity": "MILD",
      "causality": "PROBABLY RELATED"
    }
  ]
}
```

## Next Steps

- **More subjects:** "Generate 100 subjects"
- **SDTM format:** "Output as SDTM DM and AE domains"
- **Specific AE pattern:** "Include hepatotoxicity events"
- **Different phase:** "Generate a Phase I dose escalation trial"

## Related Skills

- [scenarios/trialsim/SKILL.md](../scenarios/trialsim/SKILL.md) - Full TrialSim documentation
- [scenarios/trialsim/scenarios/phase3-pivotal.md](../scenarios/trialsim/scenarios/phase3-pivotal.md) - Phase III details
