"""Pharmacy scenario events."""

from datetime import date, datetime
from enum import Enum
from typing import Any

from pydantic import BaseModel, Field


class RxEventType(str, Enum):
    """Types of pharmacy events."""

    MEMBER_ENROLLED = "member_enrolled"
    MEMBER_TERMINATED = "member_terminated"
    NEW_PRESCRIPTION = "new_prescription"
    PRESCRIPTION_TRANSFERRED = "prescription_transferred"
    CLAIM_SUBMITTED = "claim_submitted"
    CLAIM_APPROVED = "claim_approved"
    CLAIM_REJECTED = "claim_rejected"
    CLAIM_REVERSED = "claim_reversed"
    DUR_ALERT_TRIGGERED = "dur_alert"
    DUR_OVERRIDE = "dur_override"
    PA_REQUIRED = "pa_required"
    PA_SUBMITTED = "pa_submitted"
    PA_APPROVED = "pa_approved"
    PA_DENIED = "pa_denied"
    PA_APPEALED = "pa_appealed"
    SPECIALTY_ENROLLMENT = "specialty_enrollment"
    HUB_REFERRAL = "hub_referral"
    COPAY_CARD_APPLIED = "copay_card_applied"
    REFILL_DUE = "refill_due"
    REFILL_REMINDER = "refill_reminder"
    THERAPY_DISCONTINUED = "therapy_discontinued"
    FORMULARY_CHANGE = "formulary_change"
    TIER_CHANGE = "tier_change"


class RxEvent(BaseModel):
    """A pharmacy event in a timeline."""

    event_id: str
    event_type: RxEventType
    event_date: date
    event_timestamp: datetime = Field(default_factory=datetime.now)
    member_id: str
    prescription_number: str | None = None
    claim_id: str | None = None
    ndc: str | None = None
    data: dict[str, Any] = Field(default_factory=dict)
    outcome: str | None = None
    next_event_type: RxEventType | None = None


class RxTimeline(BaseModel):
    """Timeline of pharmacy events for a member."""

    member_id: str
    events: list[RxEvent] = Field(default_factory=list)

    def add_event(self, event: RxEvent) -> None:
        """Add an event to the timeline."""
        self.events.append(event)
        self.events.sort(key=lambda e: e.event_timestamp)

    def get_events_by_type(self, event_type: RxEventType) -> list[RxEvent]:
        """Get all events of a specific type."""
        return [e for e in self.events if e.event_type == event_type]

    def get_events_for_drug(self, ndc: str) -> list[RxEvent]:
        """Get all events for a specific drug."""
        return [e for e in self.events if e.ndc == ndc]

    def get_events_in_range(
        self, start_date: date, end_date: date
    ) -> list[RxEvent]:
        """Get all events within a date range."""
        return [
            e for e in self.events if start_date <= e.event_date <= end_date
        ]
