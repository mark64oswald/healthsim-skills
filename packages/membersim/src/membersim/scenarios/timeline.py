"""Timeline management for member event sequences.

Uses healthsim-core Timeline infrastructure with member-specific extensions.
"""

import uuid
from datetime import date
from typing import Any

from healthsim.temporal import EventStatus
from pydantic import BaseModel, Field

from membersim.scenarios.events import EventType


class TimelineEvent(BaseModel):
    """A concrete event instance on a member's timeline.

    Uses healthsim.temporal.EventStatus for status tracking.
    """

    timeline_event_id: str = Field(default_factory=lambda: str(uuid.uuid4())[:8])

    # Link to scenario event definition
    scenario_id: str = Field(..., description="Source scenario")
    event_definition_id: str = Field(..., description="ScenarioEvent.event_id")

    # Timing
    scheduled_date: date = Field(..., description="When event is scheduled")
    executed_date: date | None = Field(None, description="When event actually executed")

    # Event details
    event_type: EventType = Field(...)
    event_name: str = Field(...)

    # Status using core EventStatus
    status: EventStatus = Field(EventStatus.PENDING, description="Event status")

    # Generated outputs (filled after execution)
    outputs: dict[str, Any] = Field(default_factory=dict)

    # References to created/updated entities
    created_entities: dict[str, str] = Field(default_factory=dict)  # type -> id

    model_config = {"use_enum_values": True}


class MemberTimeline(BaseModel):
    """Complete timeline of events for a member.

    Manages sequences of events while maintaining compatibility with
    healthsim-core Timeline concepts.
    """

    timeline_id: str = Field(default_factory=lambda: f"TL-{uuid.uuid4().hex[:8].upper()}")
    member_id: str = Field(..., description="Associated member")

    # Source scenario(s)
    scenario_ids: list[str] = Field(default_factory=list)

    # Timeline bounds
    start_date: date = Field(..., description="Timeline start")
    end_date: date | None = Field(None, description="Timeline end (if known)")

    # Events on this timeline
    events: list[TimelineEvent] = Field(default_factory=list)

    # Current state
    current_position: int = Field(0, description="Index of next event to execute")
    is_complete: bool = Field(False)

    def add_event(self, event: TimelineEvent) -> None:
        """Add an event to the timeline."""
        self.events.append(event)
        # Keep events sorted by scheduled date
        self.events.sort(key=lambda e: e.scheduled_date)

    def get_pending_events(self) -> list[TimelineEvent]:
        """Get events that haven't been executed yet."""
        return [e for e in self.events if e.status == EventStatus.PENDING]

    def get_executed_events(self) -> list[TimelineEvent]:
        """Get events that have been executed."""
        return [e for e in self.events if e.status == EventStatus.EXECUTED]

    def get_events_on_date(self, target_date: date) -> list[TimelineEvent]:
        """Get events scheduled for a specific date."""
        return [e for e in self.events if e.scheduled_date == target_date]

    def get_events_in_range(self, start: date, end: date) -> list[TimelineEvent]:
        """Get events within a date range."""
        return [e for e in self.events if start <= e.scheduled_date <= end]

    def get_events_by_type(self, event_type: EventType) -> list[TimelineEvent]:
        """Get events of a specific type."""
        return [e for e in self.events if e.event_type == event_type]

    def get_events_by_status(self, status: EventStatus) -> list[TimelineEvent]:
        """Get events with a specific status."""
        return [e for e in self.events if e.status == status]

    def get_next_event(self) -> TimelineEvent | None:
        """Get the next scheduled event."""
        pending = self.get_pending_events()
        return pending[0] if pending else None

    def mark_executed(
        self, timeline_event_id: str, outputs: dict[str, Any] | None = None
    ) -> None:
        """Mark an event as executed."""
        for event in self.events:
            if event.timeline_event_id == timeline_event_id:
                event.status = EventStatus.EXECUTED
                event.executed_date = date.today()
                if outputs:
                    event.outputs = outputs
                break

        # Check if timeline is complete
        if not self.get_pending_events():
            self.is_complete = True

    def mark_failed(self, timeline_event_id: str, _error: str = "") -> None:
        """Mark an event as failed."""
        for event in self.events:
            if event.timeline_event_id == timeline_event_id:
                event.status = EventStatus.FAILED
                break

    def mark_skipped(self, timeline_event_id: str, _reason: str = "") -> None:
        """Mark an event as skipped."""
        for event in self.events:
            if event.timeline_event_id == timeline_event_id:
                event.status = EventStatus.SKIPPED
                break

        # Check if timeline is complete
        if not self.get_pending_events():
            self.is_complete = True

    def to_summary(self) -> dict[str, Any]:
        """Generate timeline summary."""
        return {
            "timeline_id": self.timeline_id,
            "member_id": self.member_id,
            "scenario_ids": self.scenario_ids,
            "start_date": self.start_date.isoformat(),
            "end_date": self.end_date.isoformat() if self.end_date else None,
            "total_events": len(self.events),
            "executed_events": len(self.get_executed_events()),
            "pending_events": len(self.get_pending_events()),
            "is_complete": self.is_complete,
            "event_types": list({e.event_type for e in self.events}),
        }
