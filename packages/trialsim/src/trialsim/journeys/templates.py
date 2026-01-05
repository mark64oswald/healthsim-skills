"""TrialSim journey templates.

Pre-built journey specifications for common clinical trial scenarios.
These templates can be used directly or customized for specific protocols.
"""

from healthsim.generation.journey_engine import (
    JourneySpecification,
    EventDefinition,
    DelaySpec,
    EventCondition,
    TrialEventType,
    create_simple_journey,
)


# =============================================================================
# Journey Template Definitions
# =============================================================================

TRIAL_JOURNEY_TEMPLATES = {
    "phase3-oncology-standard": {
        "journey_id": "phase3-oncology-standard",
        "name": "Phase 3 Oncology Standard Protocol",
        "description": "Standard Phase 3 oncology trial with screening, randomization, and scheduled visits",
        "products": ["trialsim"],
        "duration_days": 365,
        "events": [
            {
                "event_id": "screening",
                "name": "Screening Visit",
                "event_type": TrialEventType.SCREENING.value,
                "product": "trialsim",
                "delay": {"days": 0},
                "parameters": {
                    "pass_rate": 0.70,
                },
            },
            {
                "event_id": "randomization",
                "name": "Randomization",
                "event_type": TrialEventType.RANDOMIZATION.value,
                "product": "trialsim",
                "delay": {"days": 14, "days_min": 7, "days_max": 28},
                "depends_on": "screening",
                "conditions": [
                    {
                        "type": "event_result",
                        "event_id": "screening",
                        "field": "screen_status",
                        "operator": "equals",
                        "value": "passed",
                    }
                ],
                "parameters": {
                    "arm_weights": {"Treatment": 0.67, "Placebo": 0.33},
                },
            },
            {
                "event_id": "baseline_visit",
                "name": "Baseline Visit (Day 1)",
                "event_type": TrialEventType.SCHEDULED_VISIT.value,
                "product": "trialsim",
                "delay": {"days": 0},
                "depends_on": "randomization",
                "parameters": {
                    "visit_number": 1,
                    "visit_name": "Baseline (Day 1)",
                    "procedures": ["vital_signs", "labs", "tumor_assessment", "ecg"],
                },
            },
            {
                "event_id": "cycle1_day1",
                "name": "Cycle 1 Day 1",
                "event_type": TrialEventType.SCHEDULED_VISIT.value,
                "product": "trialsim",
                "delay": {"days": 0},
                "depends_on": "baseline_visit",
                "parameters": {
                    "visit_number": 2,
                    "visit_name": "Cycle 1 Day 1",
                    "procedures": ["vital_signs", "drug_administration"],
                },
            },
            {
                "event_id": "cycle1_day8",
                "name": "Cycle 1 Day 8",
                "event_type": TrialEventType.SCHEDULED_VISIT.value,
                "product": "trialsim",
                "delay": {"days": 7},
                "depends_on": "cycle1_day1",
                "parameters": {
                    "visit_number": 3,
                    "visit_name": "Cycle 1 Day 8",
                    "procedures": ["vital_signs", "labs"],
                },
            },
            {
                "event_id": "cycle1_day15",
                "name": "Cycle 1 Day 15",
                "event_type": TrialEventType.SCHEDULED_VISIT.value,
                "product": "trialsim",
                "delay": {"days": 14},
                "depends_on": "cycle1_day1",
                "parameters": {
                    "visit_number": 4,
                    "visit_name": "Cycle 1 Day 15",
                    "procedures": ["vital_signs", "drug_administration"],
                },
            },
            {
                "event_id": "cycle2_day1",
                "name": "Cycle 2 Day 1",
                "event_type": TrialEventType.SCHEDULED_VISIT.value,
                "product": "trialsim",
                "delay": {"days": 21},
                "depends_on": "cycle1_day1",
                "parameters": {
                    "visit_number": 5,
                    "visit_name": "Cycle 2 Day 1",
                    "procedures": ["vital_signs", "labs", "drug_administration"],
                },
            },
            {
                "event_id": "tumor_assessment_1",
                "name": "First Tumor Assessment",
                "event_type": TrialEventType.SCHEDULED_VISIT.value,
                "product": "trialsim",
                "delay": {"days": 56, "days_min": 49, "days_max": 63},
                "depends_on": "baseline_visit",
                "parameters": {
                    "visit_number": 8,
                    "visit_name": "Week 8 Tumor Assessment",
                    "procedures": ["tumor_assessment", "labs"],
                },
            },
            {
                "event_id": "tumor_assessment_2",
                "name": "Second Tumor Assessment",
                "event_type": TrialEventType.SCHEDULED_VISIT.value,
                "product": "trialsim",
                "delay": {"days": 112, "days_min": 105, "days_max": 119},
                "depends_on": "baseline_visit",
                "parameters": {
                    "visit_number": 12,
                    "visit_name": "Week 16 Tumor Assessment",
                    "procedures": ["tumor_assessment", "labs"],
                },
            },
            {
                "event_id": "end_of_treatment",
                "name": "End of Treatment Visit",
                "event_type": TrialEventType.SCHEDULED_VISIT.value,
                "product": "trialsim",
                "delay": {"days": 336, "days_min": 330, "days_max": 350},
                "depends_on": "baseline_visit",
                "parameters": {
                    "visit_number": 24,
                    "visit_name": "End of Treatment",
                    "procedures": ["vital_signs", "labs", "tumor_assessment", "ecg"],
                },
            },
            {
                "event_id": "safety_followup",
                "name": "Safety Follow-up",
                "event_type": TrialEventType.SCHEDULED_VISIT.value,
                "product": "trialsim",
                "delay": {"days": 30},
                "depends_on": "end_of_treatment",
                "parameters": {
                    "visit_number": 25,
                    "visit_name": "30-Day Safety Follow-up",
                    "procedures": ["vital_signs", "ae_assessment"],
                },
            },
        ],
    },
    
    "phase2-diabetes-dose-finding": {
        "journey_id": "phase2-diabetes-dose-finding",
        "name": "Phase 2 Diabetes Dose-Finding",
        "description": "Phase 2 dose-finding study with multiple cohorts and dose escalation",
        "products": ["trialsim"],
        "duration_days": 168,
        "events": [
            {
                "event_id": "screening",
                "name": "Screening Visit",
                "event_type": TrialEventType.SCREENING.value,
                "product": "trialsim",
                "delay": {"days": 0},
                "parameters": {
                    "pass_rate": 0.65,
                },
            },
            {
                "event_id": "run_in_start",
                "name": "Run-in Period Start",
                "event_type": TrialEventType.SCHEDULED_VISIT.value,
                "product": "trialsim",
                "delay": {"days": 7},
                "depends_on": "screening",
                "parameters": {
                    "visit_number": 1,
                    "visit_name": "Run-in Start",
                },
            },
            {
                "event_id": "randomization",
                "name": "Randomization",
                "event_type": TrialEventType.RANDOMIZATION.value,
                "product": "trialsim",
                "delay": {"days": 14},
                "depends_on": "run_in_start",
                "parameters": {
                    "arm_weights": {
                        "Low Dose": 0.25, 
                        "Medium Dose": 0.25, 
                        "High Dose": 0.25, 
                        "Placebo": 0.25
                    },
                },
            },
            {
                "event_id": "baseline",
                "name": "Baseline Visit",
                "event_type": TrialEventType.SCHEDULED_VISIT.value,
                "product": "trialsim",
                "delay": {"days": 0},
                "depends_on": "randomization",
                "parameters": {
                    "visit_number": 2,
                    "visit_name": "Baseline (Day 1)",
                    "procedures": ["vital_signs", "hba1c", "fasting_glucose", "weight"],
                },
            },
            {
                "event_id": "week2",
                "name": "Week 2 Visit",
                "event_type": TrialEventType.SCHEDULED_VISIT.value,
                "product": "trialsim",
                "delay": {"days": 14},
                "depends_on": "baseline",
                "parameters": {
                    "visit_number": 3,
                    "visit_name": "Week 2",
                    "procedures": ["vital_signs", "fasting_glucose"],
                },
            },
            {
                "event_id": "week4",
                "name": "Week 4 Visit",
                "event_type": TrialEventType.SCHEDULED_VISIT.value,
                "product": "trialsim",
                "delay": {"days": 28},
                "depends_on": "baseline",
                "parameters": {
                    "visit_number": 4,
                    "visit_name": "Week 4",
                    "procedures": ["vital_signs", "fasting_glucose", "labs"],
                },
            },
            {
                "event_id": "week8",
                "name": "Week 8 Visit",
                "event_type": TrialEventType.SCHEDULED_VISIT.value,
                "product": "trialsim",
                "delay": {"days": 56},
                "depends_on": "baseline",
                "parameters": {
                    "visit_number": 5,
                    "visit_name": "Week 8",
                    "procedures": ["vital_signs", "fasting_glucose"],
                },
            },
            {
                "event_id": "week12",
                "name": "Week 12 Primary Endpoint",
                "event_type": TrialEventType.SCHEDULED_VISIT.value,
                "product": "trialsim",
                "delay": {"days": 84},
                "depends_on": "baseline",
                "parameters": {
                    "visit_number": 6,
                    "visit_name": "Week 12 (Primary Endpoint)",
                    "procedures": ["vital_signs", "hba1c", "fasting_glucose", "weight", "labs"],
                },
            },
            {
                "event_id": "week24",
                "name": "Week 24 End of Treatment",
                "event_type": TrialEventType.SCHEDULED_VISIT.value,
                "product": "trialsim",
                "delay": {"days": 168},
                "depends_on": "baseline",
                "parameters": {
                    "visit_number": 7,
                    "visit_name": "Week 24 (End of Treatment)",
                    "procedures": ["vital_signs", "hba1c", "fasting_glucose", "weight", "labs"],
                },
            },
        ],
    },
    
    "phase1-healthy-volunteer": {
        "journey_id": "phase1-healthy-volunteer",
        "name": "Phase 1 Healthy Volunteer PK Study",
        "description": "First-in-human pharmacokinetic study with intensive PK sampling",
        "products": ["trialsim"],
        "duration_days": 28,
        "events": [
            {
                "event_id": "screening",
                "name": "Screening Visit",
                "event_type": TrialEventType.SCREENING.value,
                "product": "trialsim",
                "delay": {"days": 0},
                "parameters": {
                    "pass_rate": 0.80,
                },
            },
            {
                "event_id": "admission",
                "name": "Unit Admission",
                "event_type": TrialEventType.SCHEDULED_VISIT.value,
                "product": "trialsim",
                "delay": {"days": 7, "days_min": 3, "days_max": 14},
                "depends_on": "screening",
                "parameters": {
                    "visit_number": 1,
                    "visit_name": "Day -1 (Admission)",
                    "procedures": ["vital_signs", "labs", "ecg", "physical_exam"],
                },
            },
            {
                "event_id": "randomization",
                "name": "Randomization",
                "event_type": TrialEventType.RANDOMIZATION.value,
                "product": "trialsim",
                "delay": {"days": 1},
                "depends_on": "admission",
                "parameters": {
                    "arm_weights": {"Treatment": 0.75, "Placebo": 0.25},
                },
            },
            {
                "event_id": "dosing_day1",
                "name": "Day 1 Dosing",
                "event_type": TrialEventType.SCHEDULED_VISIT.value,
                "product": "trialsim",
                "delay": {"days": 0},
                "depends_on": "randomization",
                "parameters": {
                    "visit_number": 2,
                    "visit_name": "Day 1 (Dosing)",
                    "procedures": ["drug_administration", "pk_sampling_intensive", "vital_signs_frequent"],
                },
            },
            {
                "event_id": "pk_day2",
                "name": "Day 2 PK Sampling",
                "event_type": TrialEventType.SCHEDULED_VISIT.value,
                "product": "trialsim",
                "delay": {"days": 1},
                "depends_on": "dosing_day1",
                "parameters": {
                    "visit_number": 3,
                    "visit_name": "Day 2",
                    "procedures": ["pk_sampling", "vital_signs", "ae_assessment"],
                },
            },
            {
                "event_id": "pk_day3",
                "name": "Day 3 PK/Discharge",
                "event_type": TrialEventType.SCHEDULED_VISIT.value,
                "product": "trialsim",
                "delay": {"days": 2},
                "depends_on": "dosing_day1",
                "parameters": {
                    "visit_number": 4,
                    "visit_name": "Day 3 (Discharge)",
                    "procedures": ["pk_sampling", "vital_signs", "labs"],
                },
            },
            {
                "event_id": "followup_day7",
                "name": "Day 7 Follow-up",
                "event_type": TrialEventType.SCHEDULED_VISIT.value,
                "product": "trialsim",
                "delay": {"days": 6},
                "depends_on": "dosing_day1",
                "parameters": {
                    "visit_number": 5,
                    "visit_name": "Day 7 Follow-up",
                    "procedures": ["pk_sampling", "vital_signs", "ae_assessment"],
                },
            },
            {
                "event_id": "end_of_study",
                "name": "End of Study",
                "event_type": TrialEventType.SCHEDULED_VISIT.value,
                "product": "trialsim",
                "delay": {"days": 27},
                "depends_on": "dosing_day1",
                "parameters": {
                    "visit_number": 6,
                    "visit_name": "Day 28 (End of Study)",
                    "procedures": ["vital_signs", "labs", "ecg", "physical_exam"],
                },
            },
        ],
    },
    
    "vaccine-trial": {
        "journey_id": "vaccine-trial",
        "name": "Vaccine Efficacy Trial",
        "description": "Two-dose vaccine trial with long-term immunogenicity follow-up",
        "products": ["trialsim"],
        "duration_days": 365,
        "events": [
            {
                "event_id": "screening",
                "name": "Screening Visit",
                "event_type": TrialEventType.SCREENING.value,
                "product": "trialsim",
                "delay": {"days": 0},
                "parameters": {
                    "pass_rate": 0.85,
                },
            },
            {
                "event_id": "randomization",
                "name": "Randomization",
                "event_type": TrialEventType.RANDOMIZATION.value,
                "product": "trialsim",
                "delay": {"days": 7},
                "depends_on": "screening",
                "parameters": {
                    "arm_weights": {"Vaccine": 0.5, "Placebo": 0.5},
                },
            },
            {
                "event_id": "dose1",
                "name": "First Vaccination",
                "event_type": TrialEventType.SCHEDULED_VISIT.value,
                "product": "trialsim",
                "delay": {"days": 0},
                "depends_on": "randomization",
                "parameters": {
                    "visit_number": 1,
                    "visit_name": "Day 1 (First Dose)",
                    "procedures": ["vital_signs", "vaccination", "serology_baseline"],
                },
            },
            {
                "event_id": "dose1_day7",
                "name": "Day 7 Safety Check",
                "event_type": TrialEventType.SCHEDULED_VISIT.value,
                "product": "trialsim",
                "delay": {"days": 7},
                "depends_on": "dose1",
                "parameters": {
                    "visit_number": 2,
                    "visit_name": "Day 7",
                    "procedures": ["vital_signs", "reactogenicity_assessment"],
                },
            },
            {
                "event_id": "dose2",
                "name": "Second Vaccination",
                "event_type": TrialEventType.SCHEDULED_VISIT.value,
                "product": "trialsim",
                "delay": {"days": 21, "days_min": 21, "days_max": 28},
                "depends_on": "dose1",
                "parameters": {
                    "visit_number": 3,
                    "visit_name": "Day 21 (Second Dose)",
                    "procedures": ["vital_signs", "vaccination", "serology"],
                },
            },
            {
                "event_id": "dose2_day7",
                "name": "Day 28 Safety Check",
                "event_type": TrialEventType.SCHEDULED_VISIT.value,
                "product": "trialsim",
                "delay": {"days": 7},
                "depends_on": "dose2",
                "parameters": {
                    "visit_number": 4,
                    "visit_name": "Day 28",
                    "procedures": ["vital_signs", "reactogenicity_assessment"],
                },
            },
            {
                "event_id": "day56",
                "name": "Day 56 Immunogenicity",
                "event_type": TrialEventType.SCHEDULED_VISIT.value,
                "product": "trialsim",
                "delay": {"days": 56},
                "depends_on": "dose1",
                "parameters": {
                    "visit_number": 5,
                    "visit_name": "Day 56",
                    "procedures": ["vital_signs", "serology"],
                },
            },
            {
                "event_id": "month6",
                "name": "Month 6 Follow-up",
                "event_type": TrialEventType.SCHEDULED_VISIT.value,
                "product": "trialsim",
                "delay": {"days": 180, "days_min": 170, "days_max": 190},
                "depends_on": "dose1",
                "parameters": {
                    "visit_number": 6,
                    "visit_name": "Month 6",
                    "procedures": ["vital_signs", "serology", "ae_assessment"],
                },
            },
            {
                "event_id": "month12",
                "name": "Month 12 End of Study",
                "event_type": TrialEventType.SCHEDULED_VISIT.value,
                "product": "trialsim",
                "delay": {"days": 365, "days_min": 355, "days_max": 375},
                "depends_on": "dose1",
                "parameters": {
                    "visit_number": 7,
                    "visit_name": "Month 12 (End of Study)",
                    "procedures": ["vital_signs", "serology", "final_assessment"],
                },
            },
        ],
    },
    
    "screen-failure-journey": {
        "journey_id": "screen-failure-journey",
        "name": "Screen Failure Scenario",
        "description": "Subject who fails screening - minimal events",
        "products": ["trialsim"],
        "duration_days": 14,
        "events": [
            {
                "event_id": "screening",
                "name": "Screening Visit",
                "event_type": TrialEventType.SCREENING.value,
                "product": "trialsim",
                "delay": {"days": 0},
                "parameters": {
                    "pass_rate": 0.0,  # Force failure
                    "failure_reason": "Did not meet inclusion criteria",
                },
            },
        ],
    },
    
    "early-discontinuation": {
        "journey_id": "early-discontinuation",
        "name": "Early Discontinuation Due to AE",
        "description": "Subject who discontinues early due to adverse event",
        "products": ["trialsim"],
        "duration_days": 56,
        "events": [
            {
                "event_id": "screening",
                "name": "Screening Visit",
                "event_type": TrialEventType.SCREENING.value,
                "product": "trialsim",
                "delay": {"days": 0},
                "parameters": {"pass_rate": 1.0},
            },
            {
                "event_id": "randomization",
                "name": "Randomization",
                "event_type": TrialEventType.RANDOMIZATION.value,
                "product": "trialsim",
                "delay": {"days": 7},
                "depends_on": "screening",
            },
            {
                "event_id": "baseline",
                "name": "Baseline Visit",
                "event_type": TrialEventType.SCHEDULED_VISIT.value,
                "product": "trialsim",
                "delay": {"days": 0},
                "depends_on": "randomization",
                "parameters": {"visit_number": 1, "visit_name": "Baseline"},
            },
            {
                "event_id": "week2",
                "name": "Week 2 Visit",
                "event_type": TrialEventType.SCHEDULED_VISIT.value,
                "product": "trialsim",
                "delay": {"days": 14},
                "depends_on": "baseline",
                "parameters": {"visit_number": 2, "visit_name": "Week 2"},
            },
            {
                "event_id": "ae_onset",
                "name": "Adverse Event Onset",
                "event_type": TrialEventType.ADVERSE_EVENT.value,
                "product": "trialsim",
                "delay": {"days": 21, "days_min": 14, "days_max": 28},
                "depends_on": "baseline",
                "parameters": {
                    "term": "Severe nausea",
                    "severity": "Moderate",
                    "relationship": "Probably related",
                },
            },
            {
                "event_id": "unscheduled_ae",
                "name": "Unscheduled AE Visit",
                "event_type": TrialEventType.UNSCHEDULED_VISIT.value,
                "product": "trialsim",
                "delay": {"days": 2},
                "depends_on": "ae_onset",
                "parameters": {"reason": "AE follow-up"},
            },
            {
                "event_id": "dose_modification",
                "name": "Dose Reduction",
                "event_type": TrialEventType.DOSE_MODIFICATION.value,
                "product": "trialsim",
                "delay": {"days": 0},
                "depends_on": "unscheduled_ae",
                "parameters": {
                    "type": "dose_reduction",
                    "reason": "AE management",
                },
            },
            {
                "event_id": "withdrawal",
                "name": "Subject Withdrawal",
                "event_type": TrialEventType.WITHDRAWAL.value,
                "product": "trialsim",
                "delay": {"days": 14},
                "depends_on": "dose_modification",
                "parameters": {
                    "reason": "Adverse event",
                    "type": "investigator_decision",
                },
            },
        ],
    },
}


def get_trial_journey_template(template_id: str) -> dict | None:
    """Get a trial journey template by ID.
    
    Args:
        template_id: Template identifier (e.g., 'phase3-oncology-standard')
        
    Returns:
        Template dictionary or None if not found
    """
    return TRIAL_JOURNEY_TEMPLATES.get(template_id)


def list_trial_journey_templates() -> list[dict]:
    """List all available trial journey templates.
    
    Returns:
        List of template summaries with id, name, description
    """
    return [
        {
            "id": template_id,
            "name": template.get("name", template_id),
            "description": template.get("description", ""),
            "duration_days": template.get("duration_days", 0),
            "event_count": len(template.get("events", [])),
        }
        for template_id, template in TRIAL_JOURNEY_TEMPLATES.items()
    ]
