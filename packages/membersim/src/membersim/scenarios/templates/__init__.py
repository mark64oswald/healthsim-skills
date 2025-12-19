"""Pre-built scenario templates.

This module provides ready-to-use scenario definitions for common
healthcare member journeys.
"""

from membersim.scenarios.definition import ScenarioLibrary
from membersim.scenarios.templates.chronic import (
    DIABETIC_MEMBER_SCENARIO,
    HYPERTENSION_MANAGEMENT_SCENARIO,
)
from membersim.scenarios.templates.enrollment import (
    FAMILY_ENROLLMENT_SCENARIO,
    NEW_EMPLOYEE_SCENARIO,
    TERMINATION_COBRA_SCENARIO,
)
from membersim.scenarios.templates.episodes import (
    ELECTIVE_SURGERY_SCENARIO,
    PREVENTIVE_CARE_SCENARIO,
)
from membersim.scenarios.templates.value_based import (
    CARE_TRANSITIONS_SCENARIO,
    VALUE_BASED_CARE_PROGRAM_SCENARIO,
)

# All built-in scenarios
BUILTIN_SCENARIOS = [
    # Enrollment scenarios
    NEW_EMPLOYEE_SCENARIO,
    FAMILY_ENROLLMENT_SCENARIO,
    TERMINATION_COBRA_SCENARIO,
    # Chronic condition scenarios
    DIABETIC_MEMBER_SCENARIO,
    HYPERTENSION_MANAGEMENT_SCENARIO,
    # Episode scenarios
    PREVENTIVE_CARE_SCENARIO,
    ELECTIVE_SURGERY_SCENARIO,
    # Value-based care scenarios
    VALUE_BASED_CARE_PROGRAM_SCENARIO,
    CARE_TRANSITIONS_SCENARIO,
]


def register_builtin_scenarios() -> None:
    """Register all built-in scenarios with the ScenarioLibrary.

    Call this function to make all pre-built scenarios available
    for use with the ScenarioEngine.
    """
    for scenario in BUILTIN_SCENARIOS:
        ScenarioLibrary.register(scenario)


__all__ = [
    # Enrollment
    "NEW_EMPLOYEE_SCENARIO",
    "FAMILY_ENROLLMENT_SCENARIO",
    "TERMINATION_COBRA_SCENARIO",
    # Chronic
    "DIABETIC_MEMBER_SCENARIO",
    "HYPERTENSION_MANAGEMENT_SCENARIO",
    # Episodes
    "PREVENTIVE_CARE_SCENARIO",
    "ELECTIVE_SURGERY_SCENARIO",
    # Value-based care
    "VALUE_BASED_CARE_PROGRAM_SCENARIO",
    "CARE_TRANSITIONS_SCENARIO",
    # Collections and utilities
    "BUILTIN_SCENARIOS",
    "register_builtin_scenarios",
]
