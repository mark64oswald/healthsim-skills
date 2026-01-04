"""Tests for cohorts."""

from datetime import date

from rxmembersim.cohorts.engine import RxCohortDefinition, RxCohortEngine
from rxmembersim.cohorts.events import RxEventType


class TestRxCohortEngine:
    """Tests for RxCohortEngine."""

    def test_execute_new_therapy(self) -> None:
        """Test executing new therapy approved cohort."""
        engine = RxCohortEngine()
        cohort = engine.new_therapy_approved()
        timeline = engine.execute_cohort(cohort, "MEM001")

        assert len(timeline.events) == 3
        assert timeline.events[0].event_type == RxEventType.NEW_PRESCRIPTION
        assert timeline.events[1].event_type == RxEventType.CLAIM_SUBMITTED
        assert timeline.events[2].event_type == RxEventType.CLAIM_APPROVED
        assert timeline.events[2].outcome == "approved"

    def test_execute_pa_cohort(self) -> None:
        """Test executing PA required cohort."""
        engine = RxCohortEngine()
        cohort = engine.new_therapy_pa_required()
        timeline = engine.execute_cohort(cohort, "MEM001")

        pa_events = timeline.get_events_by_type(RxEventType.PA_APPROVED)
        assert len(pa_events) == 1

        pa_required = timeline.get_events_by_type(RxEventType.PA_REQUIRED)
        assert len(pa_required) == 1
        assert pa_required[0].data.get("reject_code") == "75"

    def test_execute_step_therapy(self) -> None:
        """Test executing step therapy cohort."""
        engine = RxCohortEngine()
        cohort = engine.new_therapy_step_therapy()
        timeline = engine.execute_cohort(cohort, "MEM001")

        # Should have multiple claim events
        claims = timeline.get_events_by_type(RxEventType.CLAIM_SUBMITTED)
        assert len(claims) >= 3

        # Final approval should satisfy step therapy
        approvals = timeline.get_events_by_type(RxEventType.CLAIM_APPROVED)
        final_approval = [e for e in approvals if e.outcome == "step_therapy_satisfied"]
        assert len(final_approval) == 1

    def test_execute_specialty_onboarding(self) -> None:
        """Test executing specialty onboarding cohort."""
        engine = RxCohortEngine()
        cohort = engine.specialty_onboarding()
        timeline = engine.execute_cohort(cohort, "MEM001")

        # Should have specialty enrollment
        specialty_events = timeline.get_events_by_type(
            RxEventType.SPECIALTY_ENROLLMENT
        )
        assert len(specialty_events) == 1

        # Should have hub referral
        hub_events = timeline.get_events_by_type(RxEventType.HUB_REFERRAL)
        assert len(hub_events) == 1

        # Should have copay card
        copay_events = timeline.get_events_by_type(RxEventType.COPAY_CARD_APPLIED)
        assert len(copay_events) == 1

    def test_execute_adherence_gap(self) -> None:
        """Test executing adherence gap cohort."""
        engine = RxCohortEngine()
        cohort = engine.adherence_gap()
        timeline = engine.execute_cohort(cohort, "MEM001")

        # Should have refill reminders
        reminders = timeline.get_events_by_type(RxEventType.REFILL_REMINDER)
        assert len(reminders) == 2

        # Should have gap days in final claim
        approvals = timeline.get_events_by_type(RxEventType.CLAIM_APPROVED)
        gap_claim = [e for e in approvals if e.data.get("gap_days")]
        assert len(gap_claim) == 1
        assert gap_claim[0].data["gap_days"] == 30

    def test_list_cohorts(self) -> None:
        """Test listing all cohorts."""
        engine = RxCohortEngine()
        cohorts = engine.list_cohorts()

        assert len(cohorts) >= 5
        assert all(isinstance(s, RxCohortDefinition) for s in cohorts)

        # Check cohort IDs are unique
        cohort_ids = [s.cohort_id for s in cohorts]
        assert len(cohort_ids) == len(set(cohort_ids))

    def test_execute_with_start_date(self) -> None:
        """Test executing cohort with custom start date."""
        engine = RxCohortEngine()
        cohort = engine.new_therapy_approved()
        start = date(2025, 6, 1)

        timeline = engine.execute_cohort(cohort, "MEM001", start_date=start)

        assert all(e.event_date == start for e in timeline.events)


class TestRxTimeline:
    """Tests for RxTimeline."""

    def test_get_events_by_type(self) -> None:
        """Test filtering events by type."""
        engine = RxCohortEngine()
        cohort = engine.new_therapy_pa_required()
        timeline = engine.execute_cohort(cohort, "MEM001")

        claims = timeline.get_events_by_type(RxEventType.CLAIM_SUBMITTED)
        assert len(claims) == 2
        assert all(e.event_type == RxEventType.CLAIM_SUBMITTED for e in claims)

    def test_events_sorted_by_timestamp(self) -> None:
        """Test that events are sorted by timestamp."""
        engine = RxCohortEngine()
        cohort = engine.new_therapy_step_therapy()
        timeline = engine.execute_cohort(cohort, "MEM001")

        timestamps = [e.event_timestamp for e in timeline.events]
        assert timestamps == sorted(timestamps)

    def test_get_events_in_range(self) -> None:
        """Test filtering events by date range."""
        engine = RxCohortEngine()
        cohort = engine.adherence_gap()
        start = date(2025, 1, 1)

        timeline = engine.execute_cohort(cohort, "MEM001", start_date=start)

        # Get events in first 30 days
        range_events = timeline.get_events_in_range(
            date(2025, 1, 1), date(2025, 1, 31)
        )
        assert len(range_events) >= 1
        assert all(
            date(2025, 1, 1) <= e.event_date <= date(2025, 1, 31)
            for e in range_events
        )


class TestRxCohortDefinition:
    """Tests for RxCohortDefinition."""

    def test_cohort_has_required_fields(self) -> None:
        """Test that cohort definitions have required fields."""
        engine = RxCohortEngine()
        for cohort in engine.list_cohorts():
            assert cohort.cohort_id
            assert cohort.cohort_name
            assert cohort.description
            assert cohort.duration_days > 0
            assert len(cohort.event_sequence) > 0
