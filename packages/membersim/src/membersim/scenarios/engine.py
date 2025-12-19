"""Scenario execution engine."""

import random
from collections.abc import Callable
from datetime import date
from typing import Any

from membersim.core.member import Member
from membersim.scenarios.definition import ScenarioDefinition
from membersim.scenarios.events import EventCondition, EventType
from membersim.scenarios.timeline import MemberTimeline, TimelineEvent


class ScenarioEngine:
    """Engine for executing scenarios and generating timelines."""

    def __init__(self, seed: int | None = None):
        self.seed = seed
        if seed is not None:
            random.seed(seed)

        # Event handlers registered by type
        self._handlers: dict[EventType, Callable] = {}

    def register_handler(self, event_type: EventType, handler: Callable) -> None:
        """Register a handler function for an event type."""
        self._handlers[event_type] = handler

    def create_timeline(
        self,
        member: Member,
        scenario: ScenarioDefinition,
        start_date: date | None = None,
        parameters: dict[str, Any] | None = None,
    ) -> MemberTimeline:
        """
        Create a timeline for a member based on a scenario.

        Args:
            member: The member to create timeline for
            scenario: Scenario definition to use
            start_date: When to start the timeline (default: member's coverage_start)
            parameters: Override scenario parameters

        Returns:
            MemberTimeline with scheduled events
        """
        timeline_start = start_date or member.coverage_start

        timeline = MemberTimeline(
            member_id=member.member_id,
            scenario_ids=[scenario.metadata.scenario_id],
            start_date=timeline_start,
        )

        # Build context for condition evaluation
        context = self._build_context(member, parameters or {})

        # Schedule events from scenario
        current_date = timeline_start
        scheduled_events: dict[str, date] = {}  # event_id -> scheduled_date

        for event_def in scenario.events:
            # Check conditions
            if not self._evaluate_conditions(event_def.conditions, context):
                continue

            # Calculate scheduled date
            if event_def.depends_on and event_def.depends_on in scheduled_events:
                base_date = scheduled_events[event_def.depends_on]
            else:
                base_date = current_date

            delay = event_def.delay.to_timedelta(self.seed)
            event_date = base_date + delay

            # Create timeline event
            timeline_event = TimelineEvent(
                scenario_id=scenario.metadata.scenario_id,
                event_definition_id=event_def.event_id,
                scheduled_date=event_date,
                event_type=event_def.event_type,
                event_name=event_def.name,
            )

            timeline.add_event(timeline_event)
            scheduled_events[event_def.event_id] = event_date

            # Advance current date for sequential events without dependencies
            if not event_def.depends_on:
                current_date = event_date

        # Set end date based on last event
        if timeline.events:
            timeline.end_date = max(e.scheduled_date for e in timeline.events)

        return timeline

    def execute_event(
        self,
        timeline: MemberTimeline,
        timeline_event: TimelineEvent,
        member: Member,
        context: dict[str, Any] | None = None,
    ) -> dict[str, Any]:
        """
        Execute a single event from a timeline.

        Args:
            timeline: The member's timeline
            timeline_event: The event to execute
            member: The member
            context: Additional context for execution

        Returns:
            Dict with execution results and any generated outputs
        """
        event_type = EventType(timeline_event.event_type)

        if event_type not in self._handlers:
            return {"status": "skipped", "reason": f"No handler for {event_type}"}

        handler = self._handlers[event_type]

        try:
            result = handler(member, timeline_event, context or {})
            timeline.mark_executed(timeline_event.timeline_event_id, result)
            return {"status": "executed", "outputs": result}
        except Exception as e:
            timeline_event.status = "failed"
            return {"status": "failed", "error": str(e)}

    def execute_timeline(
        self,
        timeline: MemberTimeline,
        member: Member,
        up_to_date: date | None = None,
    ) -> list[dict[str, Any]]:
        """
        Execute all pending events on a timeline up to a given date.

        Args:
            timeline: Timeline to execute
            member: The member
            up_to_date: Execute events up to this date (default: all pending)

        Returns:
            List of execution results
        """
        results = []
        target_date = up_to_date or date.max

        for event in timeline.get_pending_events():
            if event.scheduled_date > target_date:
                break

            result = self.execute_event(timeline, event, member)
            results.append(
                {
                    "event_id": event.timeline_event_id,
                    "event_type": event.event_type,
                    "scheduled_date": event.scheduled_date.isoformat(),
                    **result,
                }
            )

        return results

    def _build_context(self, member: Member, parameters: dict[str, Any]) -> dict[str, Any]:
        """Build context dict for condition evaluation."""
        return {
            "member": {
                "member_id": member.member_id,
                "plan_code": member.plan_code,
                "group_id": member.group_id,
                "coverage_start": member.coverage_start,
                "is_active": member.is_active,
                "is_subscriber": member.is_subscriber,
            },
            "demographics": {
                "gender": member.gender.value if hasattr(member.gender, "value") else member.gender,
                "age": member.age,
                "date_of_birth": member.birth_date,
            },
            "params": parameters,
        }

    def _evaluate_conditions(
        self, conditions: list[EventCondition], context: dict[str, Any]
    ) -> bool:
        """Evaluate all conditions (AND logic)."""
        return all(cond.evaluate(context) for cond in conditions)


def create_default_engine(seed: int | None = None) -> ScenarioEngine:
    """Create an engine with default handlers."""
    engine = ScenarioEngine(seed)

    # Register placeholder handlers (will be enhanced in later phases)
    def enrollment_handler(member: Member, _event: TimelineEvent, _context: dict) -> dict:
        return {"type": "enrollment", "member_id": member.member_id}

    def claim_handler(member: Member, _event: TimelineEvent, _context: dict) -> dict:
        return {"type": "claim", "member_id": member.member_id}

    def quality_handler(member: Member, _event: TimelineEvent, _context: dict) -> dict:
        return {"type": "quality", "member_id": member.member_id}

    engine.register_handler(EventType.NEW_ENROLLMENT, enrollment_handler)
    engine.register_handler(EventType.TERMINATION, enrollment_handler)
    engine.register_handler(EventType.CLAIM_PROFESSIONAL, claim_handler)
    engine.register_handler(EventType.CLAIM_INSTITUTIONAL, claim_handler)
    engine.register_handler(EventType.GAP_IDENTIFIED, quality_handler)
    engine.register_handler(EventType.GAP_CLOSED, quality_handler)

    return engine
