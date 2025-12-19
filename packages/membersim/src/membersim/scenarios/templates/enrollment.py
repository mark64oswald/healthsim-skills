"""Enrollment-related scenario templates."""

from membersim.scenarios.definition import ScenarioDefinition, ScenarioMetadata
from membersim.scenarios.events import DelayUnit, EventDelay, EventType, ScenarioEvent

NEW_EMPLOYEE_SCENARIO = ScenarioDefinition(
    metadata=ScenarioMetadata(
        scenario_id="new_employee_enrollment",
        name="New Employee Enrollment",
        description="Employee joins company, uses benefits over first year",
        category="enrollment",
        typical_duration_days=365,
        expected_claims=8,
    ),
    events=[
        ScenarioEvent(
            event_id="enroll",
            event_type=EventType.NEW_ENROLLMENT,
            name="Initial Enrollment",
            delay=EventDelay(value=0),
            generates=["834"],
            updates=["member", "coverage"],
        ),
        ScenarioEvent(
            event_id="pcp_visit_1",
            event_type=EventType.CLAIM_PROFESSIONAL,
            name="Initial PCP Visit",
            delay=EventDelay(value=30, unit=DelayUnit.DAYS),
            params={"procedure": "99396", "diagnosis": "Z00.00"},
            generates=["837P"],
        ),
        ScenarioEvent(
            event_id="lab_work",
            event_type=EventType.CLAIM_PROFESSIONAL,
            name="Routine Lab Work",
            delay=EventDelay(value=7, unit=DelayUnit.DAYS),
            depends_on="pcp_visit_1",
            params={"procedure": "80053", "diagnosis": "Z00.00"},
            generates=["837P"],
        ),
        ScenarioEvent(
            event_id="specialist_visit",
            event_type=EventType.CLAIM_PROFESSIONAL,
            name="Specialist Visit",
            delay=EventDelay(value=60, min_value=45, max_value=90, unit=DelayUnit.DAYS),
            depends_on="pcp_visit_1",
            params={"procedure": "99214", "diagnosis": "M54.5"},
            requires_auth=True,
            generates=["837P"],
        ),
        ScenarioEvent(
            event_id="pcp_visit_2",
            event_type=EventType.CLAIM_PROFESSIONAL,
            name="Follow-up PCP Visit",
            delay=EventDelay(value=6, unit=DelayUnit.MONTHS),
            params={"procedure": "99213", "diagnosis": "Z00.00"},
            generates=["837P"],
        ),
    ],
    parameters={
        "plan_type": "PPO",
        "include_dependents": False,
    },
)


FAMILY_ENROLLMENT_SCENARIO = ScenarioDefinition(
    metadata=ScenarioMetadata(
        scenario_id="family_enrollment",
        name="Family Enrollment with New Baby",
        description="Employee enrolls family, adds newborn mid-year",
        category="enrollment",
        typical_duration_days=365,
        expected_claims=15,
    ),
    events=[
        ScenarioEvent(
            event_id="family_enroll",
            event_type=EventType.NEW_ENROLLMENT,
            name="Family Enrollment",
            delay=EventDelay(value=0),
            params={"include_spouse": True, "include_children": True},
            generates=["834"],
        ),
        ScenarioEvent(
            event_id="spouse_preventive",
            event_type=EventType.CLAIM_PROFESSIONAL,
            name="Spouse Preventive Visit",
            delay=EventDelay(value=45, unit=DelayUnit.DAYS),
            params={"procedure": "99396", "for_dependent": "spouse"},
            generates=["837P"],
        ),
        ScenarioEvent(
            event_id="newborn_add",
            event_type=EventType.DEPENDENT_ADD,
            name="Add Newborn",
            delay=EventDelay(value=180, unit=DelayUnit.DAYS),
            params={"relationship": "child", "reason": "birth"},
            generates=["834"],
        ),
        ScenarioEvent(
            event_id="newborn_well_visit",
            event_type=EventType.CLAIM_PROFESSIONAL,
            name="Newborn Well Visit",
            delay=EventDelay(value=14, unit=DelayUnit.DAYS),
            depends_on="newborn_add",
            params={"procedure": "99391", "for_dependent": "newborn"},
            generates=["837P"],
        ),
    ],
)


TERMINATION_COBRA_SCENARIO = ScenarioDefinition(
    metadata=ScenarioMetadata(
        scenario_id="termination_cobra",
        name="Employment Termination with COBRA",
        description="Employee loses job, elects COBRA continuation",
        category="enrollment",
        typical_duration_days=180,
        expected_claims=3,
    ),
    events=[
        ScenarioEvent(
            event_id="termination",
            event_type=EventType.TERMINATION,
            name="Employment Termination",
            delay=EventDelay(value=0),
            params={"reason": "involuntary", "notice_days": 30},
            generates=["834"],
            updates=["member"],
        ),
        ScenarioEvent(
            event_id="cobra_election",
            event_type=EventType.COBRA_ELECTION,
            name="COBRA Election",
            delay=EventDelay(value=45, unit=DelayUnit.DAYS),
            depends_on="termination",
            params={"premium_multiplier": 1.02},
            generates=["834"],
        ),
        ScenarioEvent(
            event_id="cobra_claim",
            event_type=EventType.CLAIM_PROFESSIONAL,
            name="Claim During COBRA",
            delay=EventDelay(value=30, unit=DelayUnit.DAYS),
            depends_on="cobra_election",
            params={"procedure": "99213"},
            generates=["837P"],
        ),
    ],
)
