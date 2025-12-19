"""Chronic condition management scenario templates."""

from membersim.scenarios.definition import ScenarioDefinition, ScenarioMetadata
from membersim.scenarios.events import DelayUnit, EventDelay, EventType, ScenarioEvent

DIABETIC_MEMBER_SCENARIO = ScenarioDefinition(
    metadata=ScenarioMetadata(
        scenario_id="diabetic_member",
        name="Diabetic Member Management",
        description="Type 2 diabetic with ongoing care and quality measure tracking",
        category="chronic",
        typical_duration_days=365,
        expected_claims=12,
    ),
    member_constraints={
        "chronic_conditions": ["E11.9"],
        "min_age": 30,
    },
    events=[
        ScenarioEvent(
            event_id="enroll",
            event_type=EventType.NEW_ENROLLMENT,
            name="Enrollment",
            delay=EventDelay(value=0),
            opens_gaps=["CDC-A1C", "CDC-EYE", "CDC-NEPHRO"],
            generates=["834"],
        ),
        ScenarioEvent(
            event_id="pcp_visit_q1",
            event_type=EventType.CLAIM_PROFESSIONAL,
            name="Q1 PCP Visit",
            delay=EventDelay(value=14, unit=DelayUnit.DAYS),
            params={"procedure": "99214", "diagnosis": "E11.9"},
            generates=["837P"],
        ),
        ScenarioEvent(
            event_id="a1c_test",
            event_type=EventType.CLAIM_PROFESSIONAL,
            name="HbA1c Test",
            delay=EventDelay(value=0),
            depends_on="pcp_visit_q1",
            params={"procedure": "83036", "diagnosis": "E11.9"},
            closes_gaps=["CDC-A1C"],
            generates=["837P"],
        ),
        ScenarioEvent(
            event_id="gap_closed_a1c",
            event_type=EventType.GAP_CLOSED,
            name="A1C Gap Closed",
            delay=EventDelay(value=1),
            depends_on="a1c_test",
            params={"measure": "CDC-A1C"},
            updates=["measure_status"],
        ),
        ScenarioEvent(
            event_id="eye_exam",
            event_type=EventType.CLAIM_PROFESSIONAL,
            name="Diabetic Eye Exam",
            delay=EventDelay(value=60, unit=DelayUnit.DAYS),
            params={
                "procedure": "92014",
                "diagnosis": "E11.9",
                "provider_specialty": "ophthalmology",
            },
            closes_gaps=["CDC-EYE"],
            generates=["837P"],
        ),
        ScenarioEvent(
            event_id="pcp_visit_q2",
            event_type=EventType.CLAIM_PROFESSIONAL,
            name="Q2 PCP Visit",
            delay=EventDelay(value=90, unit=DelayUnit.DAYS),
            params={"procedure": "99213", "diagnosis": "E11.9"},
            generates=["837P"],
        ),
        ScenarioEvent(
            event_id="pcp_visit_q3",
            event_type=EventType.CLAIM_PROFESSIONAL,
            name="Q3 PCP Visit",
            delay=EventDelay(value=90, unit=DelayUnit.DAYS),
            depends_on="pcp_visit_q2",
            params={"procedure": "99213", "diagnosis": "E11.9"},
            generates=["837P"],
        ),
        ScenarioEvent(
            event_id="pcp_visit_q4",
            event_type=EventType.CLAIM_PROFESSIONAL,
            name="Q4 PCP Visit",
            delay=EventDelay(value=90, unit=DelayUnit.DAYS),
            depends_on="pcp_visit_q3",
            params={"procedure": "99214", "diagnosis": "E11.9"},
            generates=["837P"],
        ),
    ],
)


HYPERTENSION_MANAGEMENT_SCENARIO = ScenarioDefinition(
    metadata=ScenarioMetadata(
        scenario_id="hypertension_management",
        name="Hypertension Management",
        description="Member with hypertension requiring ongoing monitoring",
        category="chronic",
        typical_duration_days=365,
        expected_claims=8,
    ),
    member_constraints={
        "chronic_conditions": ["I10"],
        "min_age": 40,
    },
    events=[
        ScenarioEvent(
            event_id="enroll",
            event_type=EventType.NEW_ENROLLMENT,
            name="Enrollment",
            delay=EventDelay(value=0),
            opens_gaps=["CBP"],
            generates=["834"],
        ),
        ScenarioEvent(
            event_id="initial_visit",
            event_type=EventType.CLAIM_PROFESSIONAL,
            name="Initial Hypertension Visit",
            delay=EventDelay(value=21, unit=DelayUnit.DAYS),
            params={"procedure": "99214", "diagnosis": "I10"},
            generates=["837P"],
        ),
        ScenarioEvent(
            event_id="bp_followup_1",
            event_type=EventType.CLAIM_PROFESSIONAL,
            name="BP Follow-up 1",
            delay=EventDelay(value=30, unit=DelayUnit.DAYS),
            depends_on="initial_visit",
            params={"procedure": "99213", "diagnosis": "I10"},
            generates=["837P"],
        ),
        ScenarioEvent(
            event_id="bp_controlled",
            event_type=EventType.GAP_CLOSED,
            name="BP Controlled",
            delay=EventDelay(value=7),
            depends_on="bp_followup_1",
            params={"measure": "CBP", "bp_systolic": 128, "bp_diastolic": 82},
            closes_gaps=["CBP"],
        ),
        ScenarioEvent(
            event_id="quarterly_followup",
            event_type=EventType.CLAIM_PROFESSIONAL,
            name="Quarterly Follow-up",
            delay=EventDelay(value=90, unit=DelayUnit.DAYS),
            depends_on="bp_followup_1",
            params={"procedure": "99213", "diagnosis": "I10"},
            generates=["837P"],
        ),
    ],
)
