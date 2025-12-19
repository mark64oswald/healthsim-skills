"""Scenario definition and template models."""

from typing import Any

from pydantic import BaseModel, Field

from membersim.scenarios.events import EventCategory, ScenarioEvent


class ScenarioMetadata(BaseModel):
    """Metadata about a scenario."""

    scenario_id: str = Field(..., description="Unique scenario identifier")
    name: str = Field(..., description="Human-readable name")
    description: str = Field("", description="Detailed description")
    category: str = Field("general", description="Scenario category")

    version: str = Field("1.0", description="Scenario version")
    author: str = Field("MemberSim", description="Scenario author")

    # Applicability
    applicable_plan_types: list[str] = Field(default_factory=list, description="HMO, PPO, etc.")
    applicable_populations: list[str] = Field(
        default_factory=list, description="commercial, medicare, etc."
    )

    # Estimated outcomes
    typical_duration_days: int = Field(365, description="Typical scenario duration")
    expected_claims: int = Field(5, description="Expected number of claims")
    expected_cost_range: tuple = Field((1000, 5000), description="Expected cost range")


class ScenarioDefinition(BaseModel):
    """Complete scenario definition with events."""

    metadata: ScenarioMetadata = Field(...)
    events: list[ScenarioEvent] = Field(default_factory=list)

    # Member profile requirements
    member_constraints: dict[str, Any] = Field(default_factory=dict)

    # Variable parameters (can be overridden at execution)
    parameters: dict[str, Any] = Field(default_factory=dict)

    def get_events_by_category(self, category: EventCategory) -> list[ScenarioEvent]:
        """Get events filtered by category."""
        return [e for e in self.events if e.event_type.startswith(category.value)]

    def get_event(self, event_id: str) -> ScenarioEvent | None:
        """Get a specific event by ID."""
        for event in self.events:
            if event.event_id == event_id:
                return event
        return None

    def validate_dependencies(self) -> list[str]:
        """Validate that all event dependencies exist."""
        errors = []
        event_ids = {e.event_id for e in self.events}

        for event in self.events:
            if event.depends_on and event.depends_on not in event_ids:
                errors.append(
                    f"Event '{event.event_id}' depends on non-existent event '{event.depends_on}'"
                )

        return errors


class ScenarioLibrary:
    """Registry of available scenario definitions."""

    _scenarios: dict[str, ScenarioDefinition] = {}

    @classmethod
    def register(cls, scenario: ScenarioDefinition) -> None:
        """Register a scenario definition."""
        cls._scenarios[scenario.metadata.scenario_id] = scenario

    @classmethod
    def get(cls, scenario_id: str) -> ScenarioDefinition | None:
        """Get a scenario by ID."""
        return cls._scenarios.get(scenario_id)

    @classmethod
    def list_all(cls) -> list[ScenarioMetadata]:
        """List all registered scenarios."""
        return [s.metadata for s in cls._scenarios.values()]

    @classmethod
    def list_by_category(cls, category: str) -> list[ScenarioMetadata]:
        """List scenarios by category."""
        return [s.metadata for s in cls._scenarios.values() if s.metadata.category == category]
