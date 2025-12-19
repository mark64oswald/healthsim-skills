"""Tests for Scenario and Timeline Engine."""

from datetime import date, timedelta

from healthsim.temporal import EventStatus

from membersim import Member
from membersim.scenarios import (
    BUILTIN_SCENARIOS,
    MemberTimeline,
    ScenarioDefinition,
    ScenarioEngine,
    ScenarioLibrary,
    TimelineEvent,
    create_default_engine,
    register_builtin_scenarios,
)
from membersim.scenarios.events import (
    DelayUnit,
    EventCategory,
    EventCondition,
    EventDelay,
    EventType,
    ScenarioEvent,
)
from membersim.scenarios.templates import (
    DIABETIC_MEMBER_SCENARIO,
    NEW_EMPLOYEE_SCENARIO,
    PREVENTIVE_CARE_SCENARIO,
)


class TestEventTypes:
    """Test event type enumerations."""

    def test_event_type_values(self) -> None:
        """Test that key event types exist."""
        assert EventType.NEW_ENROLLMENT == "new_enrollment"
        assert EventType.CLAIM_PROFESSIONAL == "claim_professional"
        assert EventType.GAP_CLOSED == "gap_closed"

    def test_event_category_values(self) -> None:
        """Test event category values."""
        assert EventCategory.ENROLLMENT == "enrollment"
        assert EventCategory.CLAIMS == "claims"
        assert EventCategory.QUALITY == "quality"


class TestEventDelay:
    """Test event delay calculations."""

    def test_fixed_delay_days(self) -> None:
        """Test fixed delay in days."""
        delay = EventDelay(value=30, unit=DelayUnit.DAYS)
        td = delay.to_timedelta()
        assert td == timedelta(days=30)

    def test_fixed_delay_weeks(self) -> None:
        """Test fixed delay in weeks."""
        delay = EventDelay(value=2, unit=DelayUnit.WEEKS)
        td = delay.to_timedelta()
        assert td == timedelta(weeks=2)

    def test_fixed_delay_months(self) -> None:
        """Test fixed delay in months (approximated)."""
        delay = EventDelay(value=3, unit=DelayUnit.MONTHS)
        td = delay.to_timedelta()
        assert td == timedelta(days=90)  # 3 * 30

    def test_random_delay_range(self) -> None:
        """Test random delay within range."""
        delay = EventDelay(
            value=0,
            unit=DelayUnit.DAYS,
            min_value=7,
            max_value=14,
        )
        td = delay.to_timedelta(seed=42)
        assert timedelta(days=7) <= td <= timedelta(days=14)

    def test_random_delay_reproducible(self) -> None:
        """Test that same seed produces same delay."""
        delay = EventDelay(
            value=0,
            unit=DelayUnit.DAYS,
            min_value=1,
            max_value=100,
        )
        td1 = delay.to_timedelta(seed=123)
        td2 = delay.to_timedelta(seed=123)
        assert td1 == td2


class TestEventCondition:
    """Test event condition evaluation."""

    def test_condition_creation(self) -> None:
        """Test creating an event condition."""
        condition = EventCondition(
            field="age",
            operator=">=",
            value=18,
        )
        assert condition.field == "age"
        assert condition.operator == ">="
        assert condition.value == 18


class TestScenarioEvent:
    """Test scenario event model."""

    def test_event_creation(self) -> None:
        """Test creating a scenario event."""
        event = ScenarioEvent(
            event_id="evt_001",
            event_type=EventType.NEW_ENROLLMENT,
            name="New Enrollment",
            delay=EventDelay(value=0),
        )
        assert event.event_id == "evt_001"
        assert event.event_type == EventType.NEW_ENROLLMENT
        assert event.name == "New Enrollment"

    def test_event_with_dependencies(self) -> None:
        """Test event with dependencies."""
        event = ScenarioEvent(
            event_id="evt_002",
            event_type=EventType.DEMOGRAPHIC_UPDATE,
            name="PCP Assignment",
            delay=EventDelay(value=1, unit=DelayUnit.DAYS),
            depends_on="evt_001",
        )
        assert event.depends_on == "evt_001"

    def test_event_closes_gaps(self) -> None:
        """Test event that closes care gaps."""
        event = ScenarioEvent(
            event_id="evt_003",
            event_type=EventType.CLAIM_PROFESSIONAL,
            name="Preventive Visit",
            delay=EventDelay(value=30, unit=DelayUnit.DAYS),
            closes_gaps=["AWC", "WCV"],
        )
        assert "AWC" in event.closes_gaps
        assert "WCV" in event.closes_gaps


class TestScenarioDefinition:
    """Test scenario definition model."""

    def test_scenario_definition_creation(self) -> None:
        """Test creating a scenario definition."""
        assert NEW_EMPLOYEE_SCENARIO.metadata.scenario_id == "new_employee_enrollment"
        assert NEW_EMPLOYEE_SCENARIO.metadata.name == "New Employee Enrollment"
        assert len(NEW_EMPLOYEE_SCENARIO.events) > 0

    def test_scenario_has_events(self) -> None:
        """Test that scenarios have defined events."""
        for scenario in BUILTIN_SCENARIOS:
            assert len(scenario.events) > 0
            assert scenario.metadata.scenario_id is not None


class TestScenarioLibrary:
    """Test scenario library registry."""

    def test_register_and_get(self) -> None:
        """Test registering and retrieving scenarios."""
        register_builtin_scenarios()

        scenario = ScenarioLibrary.get("new_employee_enrollment")
        assert scenario is not None
        assert scenario.metadata.scenario_id == "new_employee_enrollment"

    def test_list_scenarios(self) -> None:
        """Test listing all registered scenarios."""
        register_builtin_scenarios()

        all_metadata = ScenarioLibrary.list_all()
        all_ids = [m.scenario_id for m in all_metadata]
        assert "new_employee_enrollment" in all_ids
        assert "diabetic_member" in all_ids

    def test_list_by_category(self) -> None:
        """Test filtering by category."""
        register_builtin_scenarios()

        enrollment_scenarios = ScenarioLibrary.list_by_category("enrollment")
        assert len(enrollment_scenarios) > 0


class TestTimelineEvent:
    """Test timeline event model."""

    def test_timeline_event_creation(self) -> None:
        """Test creating a timeline event."""
        event = TimelineEvent(
            timeline_event_id="tl_001",
            scenario_id="new_employee_enrollment",
            event_definition_id="evt_001",
            scheduled_date=date(2024, 1, 15),
            event_type=EventType.NEW_ENROLLMENT,
            event_name="New Enrollment",
        )
        assert event.timeline_event_id == "tl_001"
        assert event.status == EventStatus.PENDING
        assert event.scheduled_date == date(2024, 1, 15)


class TestMemberTimeline:
    """Test member timeline management."""

    def test_timeline_creation(self) -> None:
        """Test creating a timeline."""
        timeline = MemberTimeline(
            member_id="MEM001",
            start_date=date(2024, 1, 1),
        )
        assert timeline.member_id == "MEM001"
        assert len(timeline.events) == 0

    def test_add_event(self) -> None:
        """Test adding events to timeline."""
        timeline = MemberTimeline(
            member_id="MEM001",
            start_date=date(2024, 1, 1),
        )
        event = TimelineEvent(
            timeline_event_id="tl_001",
            scenario_id="test",
            event_definition_id="evt_001",
            scheduled_date=date(2024, 1, 15),
            event_type=EventType.NEW_ENROLLMENT,
            event_name="New Enrollment",
        )
        timeline.add_event(event)
        assert len(timeline.events) == 1

    def test_get_pending_events(self) -> None:
        """Test getting pending events."""
        timeline = MemberTimeline(
            member_id="MEM001",
            start_date=date(2024, 1, 1),
            events=[
                TimelineEvent(
                    timeline_event_id="tl_001",
                    scenario_id="test",
                    event_definition_id="evt_001",
                    scheduled_date=date(2024, 1, 15),
                    event_type=EventType.NEW_ENROLLMENT,
                    event_name="New Enrollment",
                    status=EventStatus.EXECUTED,
                ),
                TimelineEvent(
                    timeline_event_id="tl_002",
                    scenario_id="test",
                    event_definition_id="evt_002",
                    scheduled_date=date(2024, 2, 15),
                    event_type=EventType.CLAIM_PROFESSIONAL,
                    event_name="Office Visit",
                    status=EventStatus.PENDING,
                ),
            ],
        )
        pending = timeline.get_pending_events()
        assert len(pending) == 1
        assert pending[0].timeline_event_id == "tl_002"

    def test_get_events_in_range(self) -> None:
        """Test filtering events by date range."""
        timeline = MemberTimeline(
            member_id="MEM001",
            start_date=date(2024, 1, 1),
            events=[
                TimelineEvent(
                    timeline_event_id="tl_001",
                    scenario_id="test",
                    event_definition_id="evt_001",
                    scheduled_date=date(2024, 1, 15),
                    event_type=EventType.NEW_ENROLLMENT,
                    event_name="New Enrollment",
                ),
                TimelineEvent(
                    timeline_event_id="tl_002",
                    scenario_id="test",
                    event_definition_id="evt_002",
                    scheduled_date=date(2024, 3, 15),
                    event_type=EventType.CLAIM_PROFESSIONAL,
                    event_name="Office Visit",
                ),
            ],
        )
        events = timeline.get_events_in_range(
            start=date(2024, 1, 1),
            end=date(2024, 2, 28),
        )
        assert len(events) == 1
        assert events[0].timeline_event_id == "tl_001"


class TestScenarioEngine:
    """Test scenario execution engine."""

    def test_engine_creation(self) -> None:
        """Test creating an engine."""
        engine = ScenarioEngine(seed=42)
        assert engine is not None

    def test_create_default_engine(self) -> None:
        """Test default engine factory."""
        engine = create_default_engine(seed=42)
        assert engine is not None

    def test_create_timeline_from_scenario(self, sample_member: Member) -> None:
        """Test creating a timeline from a scenario."""
        engine = ScenarioEngine(seed=42)
        register_builtin_scenarios()

        timeline = engine.create_timeline(
            member=sample_member,
            scenario=NEW_EMPLOYEE_SCENARIO,
            start_date=date(2024, 1, 1),
        )

        assert timeline is not None
        assert timeline.member_id == sample_member.member_id
        assert len(timeline.events) > 0

    def test_timeline_events_ordered_by_date(self, sample_member: Member) -> None:
        """Test that timeline events are ordered by date."""
        engine = ScenarioEngine(seed=42)

        timeline = engine.create_timeline(
            member=sample_member,
            scenario=NEW_EMPLOYEE_SCENARIO,
            start_date=date(2024, 1, 1),
        )

        dates = [e.scheduled_date for e in timeline.events]
        assert dates == sorted(dates)

    def test_execute_single_event(self, sample_member: Member) -> None:
        """Test executing a single event."""
        engine = ScenarioEngine(seed=42)
        outputs: list[dict] = []

        def capture_handler(member: Member, event: TimelineEvent, context: dict) -> dict:
            outputs.append({"event_type": event.event_type})
            return {"status": "success"}

        engine.register_handler(EventType.NEW_ENROLLMENT, capture_handler)

        timeline = engine.create_timeline(
            member=sample_member,
            scenario=NEW_EMPLOYEE_SCENARIO,
            start_date=date(2024, 1, 1),
        )

        # Execute first event
        first_event = timeline.events[0]
        engine.execute_event(
            timeline=timeline,
            timeline_event=first_event,
            member=sample_member,
            context={},
        )

        # Check event was marked executed
        executed_event = next(
            e for e in timeline.events if e.timeline_event_id == first_event.timeline_event_id
        )
        assert executed_event.status == EventStatus.EXECUTED


class TestBuiltinScenarios:
    """Test built-in scenario templates."""

    def test_all_scenarios_valid(self) -> None:
        """Test that all built-in scenarios are valid definitions."""
        for scenario in BUILTIN_SCENARIOS:
            assert isinstance(scenario, ScenarioDefinition)
            assert scenario.metadata.scenario_id is not None
            assert scenario.metadata.name is not None
            assert len(scenario.events) > 0

    def test_new_employee_scenario(self) -> None:
        """Test new employee scenario structure."""
        scenario = NEW_EMPLOYEE_SCENARIO
        assert scenario.metadata.category == "enrollment"

        # Should start with enrollment event
        first_event = scenario.events[0]
        assert first_event.event_type == EventType.NEW_ENROLLMENT

    def test_diabetic_member_scenario(self) -> None:
        """Test diabetic member scenario structure."""
        scenario = DIABETIC_MEMBER_SCENARIO
        assert scenario.metadata.category == "chronic"

        # Should have professional claim events
        event_types = [e.event_type for e in scenario.events]
        assert EventType.CLAIM_PROFESSIONAL in event_types

    def test_preventive_care_scenario(self) -> None:
        """Test preventive care scenario structure."""
        scenario = PREVENTIVE_CARE_SCENARIO
        assert scenario.metadata.category == "preventive"

        # Should have claim events
        event_types = [e.event_type for e in scenario.events]
        assert EventType.CLAIM_PROFESSIONAL in event_types

    def test_scenario_event_dependencies_valid(self) -> None:
        """Test that event dependencies reference valid events."""
        for scenario in BUILTIN_SCENARIOS:
            event_ids = {e.event_id for e in scenario.events}
            for event in scenario.events:
                if event.depends_on:
                    assert event.depends_on in event_ids, (
                        f"Invalid dependency {event.depends_on} in {scenario.metadata.scenario_id}"
                    )
