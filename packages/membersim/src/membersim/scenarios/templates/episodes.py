"""Episode-based scenario templates."""

from membersim.scenarios.definition import ScenarioDefinition, ScenarioMetadata
from membersim.scenarios.events import (
    DelayUnit,
    EventCondition,
    EventDelay,
    EventType,
    ScenarioEvent,
)

PREVENTIVE_CARE_SCENARIO = ScenarioDefinition(
    metadata=ScenarioMetadata(
        scenario_id="preventive_care",
        name="Annual Preventive Care",
        description="Comprehensive preventive care with screenings",
        category="preventive",
        typical_duration_days=60,
        expected_claims=4,
    ),
    events=[
        ScenarioEvent(
            event_id="wellness_visit",
            event_type=EventType.CLAIM_PROFESSIONAL,
            name="Annual Wellness Visit",
            delay=EventDelay(value=0),
            params={"procedure": "99396", "diagnosis": "Z00.00"},
            generates=["837P"],
        ),
        ScenarioEvent(
            event_id="lab_panel",
            event_type=EventType.CLAIM_PROFESSIONAL,
            name="Preventive Lab Panel",
            delay=EventDelay(value=0),
            depends_on="wellness_visit",
            params={
                "procedures": ["80053", "80061", "85025"],
                "diagnosis": "Z00.00",
            },
            generates=["837P"],
        ),
        ScenarioEvent(
            event_id="mammogram",
            event_type=EventType.CLAIM_PROFESSIONAL,
            name="Screening Mammogram",
            delay=EventDelay(value=14, unit=DelayUnit.DAYS),
            conditions=[
                EventCondition(field="demographics.gender", operator="==", value="F"),
                EventCondition(field="demographics.age", operator=">=", value=50),
            ],
            params={"procedure": "77067", "diagnosis": "Z12.31"},
            closes_gaps=["BCS"],
            generates=["837P"],
        ),
        ScenarioEvent(
            event_id="colonoscopy",
            event_type=EventType.CLAIM_PROFESSIONAL,
            name="Screening Colonoscopy",
            delay=EventDelay(value=30, unit=DelayUnit.DAYS),
            conditions=[
                EventCondition(field="demographics.age", operator=">=", value=50),
            ],
            params={"procedure": "45378", "diagnosis": "Z12.11"},
            closes_gaps=["COL"],
            requires_auth=True,
            generates=["837P"],
        ),
    ],
)


ELECTIVE_SURGERY_SCENARIO = ScenarioDefinition(
    metadata=ScenarioMetadata(
        scenario_id="elective_surgery",
        name="Elective Surgical Episode",
        description="Complete elective surgery episode with prior auth",
        category="episode",
        typical_duration_days=90,
        expected_claims=8,
    ),
    parameters={
        "surgery_procedure": "27130",  # Hip replacement
        "surgery_diagnosis": "M16.11",  # Osteoarthritis
    },
    events=[
        ScenarioEvent(
            event_id="eligibility_check",
            event_type=EventType.ELIGIBILITY_INQUIRY,
            name="Pre-Service Eligibility Check",
            delay=EventDelay(value=0),
            generates=["270"],
        ),
        ScenarioEvent(
            event_id="eligibility_response",
            event_type=EventType.ELIGIBILITY_RESPONSE,
            name="Eligibility Confirmed",
            delay=EventDelay(value=0),
            depends_on="eligibility_check",
            generates=["271"],
        ),
        ScenarioEvent(
            event_id="auth_request",
            event_type=EventType.AUTH_REQUEST,
            name="Prior Authorization Request",
            delay=EventDelay(value=1),
            params={"service_type": "INPATIENT", "requested_days": 3},
            generates=["278"],
        ),
        ScenarioEvent(
            event_id="auth_approved",
            event_type=EventType.AUTH_APPROVED,
            name="Authorization Approved",
            delay=EventDelay(value=3, unit=DelayUnit.DAYS),
            depends_on="auth_request",
            params={"approved_days": 3},
            generates=["278"],
        ),
        ScenarioEvent(
            event_id="pre_op",
            event_type=EventType.CLAIM_PROFESSIONAL,
            name="Pre-Op Evaluation",
            delay=EventDelay(value=7, unit=DelayUnit.DAYS),
            depends_on="auth_approved",
            params={"procedure": "99214", "diagnosis": "M16.11"},
            generates=["837P"],
        ),
        ScenarioEvent(
            event_id="surgery",
            event_type=EventType.CLAIM_INSTITUTIONAL,
            name="Surgical Admission",
            delay=EventDelay(value=14, unit=DelayUnit.DAYS),
            depends_on="pre_op",
            params={
                "procedure": "27130",
                "diagnosis": "M16.11",
                "los_days": 3,
                "type_of_bill": "0111",
            },
            generates=["837I"],
            updates=["accumulator"],
        ),
        ScenarioEvent(
            event_id="payment",
            event_type=EventType.PAYMENT,
            name="Claim Payment",
            delay=EventDelay(value=30, unit=DelayUnit.DAYS),
            depends_on="surgery",
            generates=["835"],
            updates=["accumulator"],
        ),
        ScenarioEvent(
            event_id="post_op",
            event_type=EventType.CLAIM_PROFESSIONAL,
            name="Post-Op Follow-up",
            delay=EventDelay(value=14, unit=DelayUnit.DAYS),
            depends_on="surgery",
            params={"procedure": "99213", "diagnosis": "Z96.64"},
            generates=["837P"],
        ),
    ],
)
