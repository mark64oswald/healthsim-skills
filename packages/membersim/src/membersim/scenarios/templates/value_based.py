"""Value-based care scenario templates.

These scenarios demonstrate care management programs, quality incentives,
and value-based payment arrangements.
"""

from membersim.scenarios.definition import ScenarioDefinition, ScenarioMetadata
from membersim.scenarios.events import (
    DelayUnit,
    EventDelay,
    EventType,
    ScenarioEvent,
)

VALUE_BASED_CARE_PROGRAM_SCENARIO = ScenarioDefinition(
    metadata=ScenarioMetadata(
        scenario_id="value_based_care_program",
        name="Value-Based Care Program",
        description="High-risk member in care management program with quality tracking",
        category="value_based",
        typical_duration_days=180,
        expected_claims=15,
    ),
    member_constraints={
        "risk_score_min": 1.5,  # HCC risk score threshold
        "chronic_conditions": ["E11.9", "I10", "J44.9"],  # Diabetes, HTN, COPD
        "min_age": 45,
    },
    parameters={
        "care_manager_assigned": True,
        "quality_bonus_eligible": True,
        "shared_savings_program": True,
    },
    events=[
        # Initial risk stratification and program enrollment
        ScenarioEvent(
            event_id="risk_stratification",
            event_type=EventType.CARE_MANAGEMENT,
            name="Risk Stratification",
            delay=EventDelay(value=0),
            params={
                "activity": "risk_assessment",
                "hcc_categories": ["19", "85", "111"],  # DM with complications, COPD, CHF
                "risk_score": 2.1,
            },
        ),
        ScenarioEvent(
            event_id="care_mgmt_enrollment",
            event_type=EventType.CARE_MANAGEMENT,
            name="Care Management Enrollment",
            delay=EventDelay(value=1),
            depends_on="risk_stratification",
            params={
                "activity": "program_enrollment",
                "program": "Chronic Care Management",
                "care_manager": "CM001",
            },
            opens_gaps=["AWV", "CDC-A1C", "CBP", "SPR-E"],
        ),
        # Initial comprehensive assessment
        ScenarioEvent(
            event_id="comprehensive_assessment",
            event_type=EventType.CLAIM_PROFESSIONAL,
            name="Annual Wellness Visit",
            delay=EventDelay(value=7, unit=DelayUnit.DAYS),
            params={
                "procedure": "G0438",  # Initial AWV
                "diagnosis": "Z00.00",
                "quality_measure": "AWV",
            },
            closes_gaps=["AWV"],
            generates=["837P"],
        ),
        ScenarioEvent(
            event_id="care_plan_created",
            event_type=EventType.CARE_MANAGEMENT,
            name="Care Plan Created",
            delay=EventDelay(value=0),
            depends_on="comprehensive_assessment",
            params={
                "activity": "care_plan",
                "goals": ["A1C < 8%", "BP < 140/90", "COPD action plan"],
            },
        ),
        # CCM billing (monthly)
        ScenarioEvent(
            event_id="ccm_month_1",
            event_type=EventType.CLAIM_PROFESSIONAL,
            name="CCM Services Month 1",
            delay=EventDelay(value=30, unit=DelayUnit.DAYS),
            params={
                "procedure": "99490",  # CCM, 20+ minutes
                "diagnosis": "E11.9",
                "time_spent": 25,
            },
            generates=["837P"],
        ),
        # Diabetes management visit
        ScenarioEvent(
            event_id="diabetes_visit",
            event_type=EventType.CLAIM_PROFESSIONAL,
            name="Diabetes Management Visit",
            delay=EventDelay(value=14, unit=DelayUnit.DAYS),
            depends_on="comprehensive_assessment",
            params={"procedure": "99214", "diagnosis": "E11.9"},
            generates=["837P"],
        ),
        ScenarioEvent(
            event_id="a1c_test",
            event_type=EventType.CLAIM_PROFESSIONAL,
            name="HbA1c Test",
            delay=EventDelay(value=0),
            depends_on="diabetes_visit",
            params={
                "procedure": "83036",
                "diagnosis": "E11.9",
                "result_value": 7.2,
                "quality_measure": "CDC-A1C",
            },
            closes_gaps=["CDC-A1C"],
            generates=["837P"],
        ),
        # COPD management
        ScenarioEvent(
            event_id="copd_visit",
            event_type=EventType.CLAIM_PROFESSIONAL,
            name="COPD Management Visit",
            delay=EventDelay(value=45, unit=DelayUnit.DAYS),
            params={"procedure": "99214", "diagnosis": "J44.9"},
            generates=["837P"],
        ),
        ScenarioEvent(
            event_id="spirometry",
            event_type=EventType.CLAIM_PROFESSIONAL,
            name="Spirometry Testing",
            delay=EventDelay(value=0),
            depends_on="copd_visit",
            params={
                "procedure": "94010",
                "diagnosis": "J44.9",
                "quality_measure": "SPR-E",
            },
            closes_gaps=["SPR-E"],
            generates=["837P"],
        ),
        # CCM billing month 2
        ScenarioEvent(
            event_id="ccm_month_2",
            event_type=EventType.CLAIM_PROFESSIONAL,
            name="CCM Services Month 2",
            delay=EventDelay(value=60, unit=DelayUnit.DAYS),
            params={
                "procedure": "99490",
                "diagnosis": "E11.9",
                "time_spent": 30,
            },
            generates=["837P"],
        ),
        # Care coordination call
        ScenarioEvent(
            event_id="care_coord_call",
            event_type=EventType.CARE_MANAGEMENT,
            name="Care Coordination Call",
            delay=EventDelay(value=75, unit=DelayUnit.DAYS),
            params={
                "activity": "phone_outreach",
                "duration_minutes": 15,
                "topics": ["medication_adherence", "bp_monitoring"],
            },
        ),
        # Blood pressure follow-up
        ScenarioEvent(
            event_id="bp_followup",
            event_type=EventType.CLAIM_PROFESSIONAL,
            name="BP Follow-up Visit",
            delay=EventDelay(value=90, unit=DelayUnit.DAYS),
            params={
                "procedure": "99213",
                "diagnosis": "I10",
                "bp_reading": "134/82",
                "quality_measure": "CBP",
            },
            closes_gaps=["CBP"],
            generates=["837P"],
        ),
        # CCM month 3
        ScenarioEvent(
            event_id="ccm_month_3",
            event_type=EventType.CLAIM_PROFESSIONAL,
            name="CCM Services Month 3",
            delay=EventDelay(value=90, unit=DelayUnit.DAYS),
            params={
                "procedure": "99490",
                "diagnosis": "E11.9",
                "time_spent": 22,
            },
            generates=["837P"],
        ),
        # Quality incentive payment
        ScenarioEvent(
            event_id="quality_incentive",
            event_type=EventType.QUALITY_BONUS,
            name="Quality Incentive Payment",
            delay=EventDelay(value=180, unit=DelayUnit.DAYS),
            params={
                "measures_met": ["AWV", "CDC-A1C", "CBP", "SPR-E"],
                "bonus_amount": 250.00,
                "payer_program": "MSSP",
            },
            updates=["provider_incentive"],
        ),
    ],
)


CARE_TRANSITIONS_SCENARIO = ScenarioDefinition(
    metadata=ScenarioMetadata(
        scenario_id="care_transitions",
        name="Care Transitions Program",
        description="Post-discharge care transitions to prevent readmission",
        category="value_based",
        typical_duration_days=45,
        expected_claims=6,
    ),
    member_constraints={
        "recent_admission": True,
        "readmission_risk": "high",
    },
    events=[
        # Hospital discharge
        ScenarioEvent(
            event_id="hospital_discharge",
            event_type=EventType.CLAIM_INSTITUTIONAL,
            name="Hospital Discharge",
            delay=EventDelay(value=0),
            params={
                "procedure": "99238",  # Discharge management
                "diagnosis": "I50.9",  # Heart failure
                "los_days": 4,
                "discharge_disposition": "01",  # Home
            },
            generates=["837I"],
            opens_gaps=["TCM"],
        ),
        # TCM phone call within 2 days
        ScenarioEvent(
            event_id="tcm_call",
            event_type=EventType.CARE_MANAGEMENT,
            name="TCM Phone Contact",
            delay=EventDelay(value=2, unit=DelayUnit.DAYS),
            depends_on="hospital_discharge",
            params={
                "activity": "tcm_phone",
                "topics": ["medication_reconciliation", "follow_up_scheduling"],
            },
        ),
        # Home health visit
        ScenarioEvent(
            event_id="home_health_visit",
            event_type=EventType.CLAIM_INSTITUTIONAL,
            name="Home Health Visit",
            delay=EventDelay(value=3, unit=DelayUnit.DAYS),
            depends_on="hospital_discharge",
            params={
                "procedure": "G0299",  # Home health skilled nursing
                "diagnosis": "I50.9",
                "type_of_bill": "0321",
            },
            generates=["837I"],
        ),
        # TCM face-to-face within 7 days
        ScenarioEvent(
            event_id="tcm_visit",
            event_type=EventType.CLAIM_PROFESSIONAL,
            name="TCM Face-to-Face Visit",
            delay=EventDelay(value=7, unit=DelayUnit.DAYS),
            depends_on="hospital_discharge",
            params={
                "procedure": "99495",  # TCM, moderate complexity
                "diagnosis": "I50.9",
            },
            closes_gaps=["TCM"],
            generates=["837P"],
        ),
        # Cardiology follow-up
        ScenarioEvent(
            event_id="cardiology_followup",
            event_type=EventType.CLAIM_PROFESSIONAL,
            name="Cardiology Follow-up",
            delay=EventDelay(value=14, unit=DelayUnit.DAYS),
            depends_on="hospital_discharge",
            params={
                "procedure": "99214",
                "diagnosis": "I50.9",
                "provider_specialty": "cardiology",
            },
            generates=["837P"],
        ),
        # 30-day milestone - no readmission
        ScenarioEvent(
            event_id="no_readmission",
            event_type=EventType.MILESTONE,
            name="30-Day No Readmission",
            delay=EventDelay(value=30, unit=DelayUnit.DAYS),
            depends_on="hospital_discharge",
            params={
                "milestone": "readmission_avoided",
                "quality_measure": "PCR",  # Potentially preventable readmission
            },
            updates=["quality_score"],
        ),
    ],
)
