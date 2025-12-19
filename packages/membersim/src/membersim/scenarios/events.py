"""Base event model and payer-domain event types."""

import random
from datetime import timedelta
from enum import Enum
from typing import Any

from pydantic import BaseModel, Field


class EventCategory(str, Enum):
    """High-level event categories."""

    ENROLLMENT = "enrollment"
    CLAIMS = "claims"
    ELIGIBILITY = "eligibility"
    AUTHORIZATION = "authorization"
    QUALITY = "quality"
    VBC = "vbc"


class EventType(str, Enum):
    """Specific event types within categories."""

    # Enrollment events
    NEW_ENROLLMENT = "new_enrollment"
    DEPENDENT_ADD = "dependent_add"
    DEPENDENT_REMOVE = "dependent_remove"
    PLAN_CHANGE = "plan_change"
    DEMOGRAPHIC_UPDATE = "demographic_update"
    TERMINATION = "termination"
    COBRA_ELECTION = "cobra_election"

    # Claims events
    CLAIM_PROFESSIONAL = "claim_professional"
    CLAIM_INSTITUTIONAL = "claim_institutional"
    CLAIM_PHARMACY = "claim_pharmacy"
    PAYMENT = "payment"

    # Eligibility events
    ELIGIBILITY_INQUIRY = "eligibility_inquiry"
    ELIGIBILITY_RESPONSE = "eligibility_response"

    # Authorization events
    AUTH_REQUEST = "auth_request"
    AUTH_APPROVED = "auth_approved"
    AUTH_DENIED = "auth_denied"
    AUTH_MODIFIED = "auth_modified"

    # Quality events
    GAP_IDENTIFIED = "gap_identified"
    GAP_CLOSED = "gap_closed"
    OUTREACH_SENT = "outreach_sent"

    # VBC events
    ATTRIBUTION = "attribution"
    CAPITATION_PAYMENT = "capitation_payment"
    RISK_SCORE_UPDATE = "risk_score_update"
    CARE_MANAGEMENT = "care_management"
    QUALITY_BONUS = "quality_bonus"
    MILESTONE = "milestone"


class DelayUnit(str, Enum):
    """Units for event delays."""

    DAYS = "days"
    WEEKS = "weeks"
    MONTHS = "months"


class EventDelay(BaseModel):
    """Configurable delay between events."""

    value: int = Field(0, description="Delay amount")
    unit: DelayUnit = Field(DelayUnit.DAYS)
    min_value: int | None = Field(None, description="Minimum for random range")
    max_value: int | None = Field(None, description="Maximum for random range")

    def to_timedelta(self, seed: int | None = None) -> timedelta:
        """Convert delay to timedelta, with optional randomization."""
        if seed is not None:
            random.seed(seed)

        if self.min_value is not None and self.max_value is not None:
            actual_value = random.randint(self.min_value, self.max_value)
        else:
            actual_value = self.value

        if self.unit == DelayUnit.DAYS:
            return timedelta(days=actual_value)
        elif self.unit == DelayUnit.WEEKS:
            return timedelta(weeks=actual_value)
        elif self.unit == DelayUnit.MONTHS:
            return timedelta(days=actual_value * 30)  # Approximate
        return timedelta(days=actual_value)


class EventCondition(BaseModel):
    """Condition that must be met for event to execute."""

    field: str = Field(..., description="Field to check (e.g., 'member.gender')")
    operator: str = Field("==", description="Comparison operator")
    value: Any = Field(..., description="Value to compare against")

    def evaluate(self, context: dict[str, Any]) -> bool:
        """Evaluate condition against context."""
        # Simple dot-notation field access
        parts = self.field.split(".")
        current = context
        for part in parts:
            if isinstance(current, dict):
                current = current.get(part)
            elif hasattr(current, part):
                current = getattr(current, part)
            else:
                return False

        if self.operator == "==":
            return current == self.value
        elif self.operator == "!=":
            return current != self.value
        elif self.operator == ">=":
            return current >= self.value
        elif self.operator == "<=":
            return current <= self.value
        elif self.operator == ">":
            return current > self.value
        elif self.operator == "<":
            return current < self.value
        elif self.operator == "in":
            return current in self.value
        elif self.operator == "contains":
            return self.value in current
        return False


class ScenarioEvent(BaseModel):
    """A single event within a scenario definition."""

    event_id: str = Field(..., description="Unique identifier within scenario")
    event_type: EventType = Field(..., description="Type of event")
    name: str = Field(..., description="Human-readable event name")

    delay: EventDelay = Field(default_factory=EventDelay)
    conditions: list[EventCondition] = Field(default_factory=list)

    # Event-specific parameters
    params: dict[str, Any] = Field(default_factory=dict)

    # What this event produces/affects
    generates: list[str] = Field(default_factory=list, description="Output formats generated")
    updates: list[str] = Field(default_factory=list, description="Models updated")
    closes_gaps: list[str] = Field(default_factory=list, description="Quality gaps closed")
    opens_gaps: list[str] = Field(default_factory=list, description="Quality gaps opened")

    # Dependencies
    requires_auth: bool = Field(False, description="Requires prior authorization")
    depends_on: str | None = Field(None, description="Event ID this depends on")

    model_config = {"use_enum_values": True}
