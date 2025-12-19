"""Scenario and timeline engine for synthetic member data generation.

This module provides a pathway-based event generation system for creating
realistic member healthcare journeys.
"""

from healthsim.temporal import EventStatus

from membersim.scenarios.definition import (
    ScenarioDefinition,
    ScenarioLibrary,
    ScenarioMetadata,
)
from membersim.scenarios.engine import ScenarioEngine, create_default_engine
from membersim.scenarios.events import (
    DelayUnit,
    EventCategory,
    EventCondition,
    EventDelay,
    EventType,
    ScenarioEvent,
)
from membersim.scenarios.templates import (
    BUILTIN_SCENARIOS,
    DIABETIC_MEMBER_SCENARIO,
    ELECTIVE_SURGERY_SCENARIO,
    FAMILY_ENROLLMENT_SCENARIO,
    HYPERTENSION_MANAGEMENT_SCENARIO,
    NEW_EMPLOYEE_SCENARIO,
    PREVENTIVE_CARE_SCENARIO,
    TERMINATION_COBRA_SCENARIO,
    register_builtin_scenarios,
)
from membersim.scenarios.timeline import MemberTimeline, TimelineEvent

__all__ = [
    # Event types and building blocks
    "EventType",
    "EventStatus",
    "EventCategory",
    "DelayUnit",
    "EventDelay",
    "EventCondition",
    "ScenarioEvent",
    # Scenario definition
    "ScenarioMetadata",
    "ScenarioDefinition",
    "ScenarioLibrary",
    # Timeline
    "TimelineEvent",
    "MemberTimeline",
    # Engine
    "ScenarioEngine",
    "create_default_engine",
    # Built-in scenarios
    "BUILTIN_SCENARIOS",
    "NEW_EMPLOYEE_SCENARIO",
    "FAMILY_ENROLLMENT_SCENARIO",
    "TERMINATION_COBRA_SCENARIO",
    "DIABETIC_MEMBER_SCENARIO",
    "HYPERTENSION_MANAGEMENT_SCENARIO",
    "PREVENTIVE_CARE_SCENARIO",
    "ELECTIVE_SURGERY_SCENARIO",
    "register_builtin_scenarios",
]
