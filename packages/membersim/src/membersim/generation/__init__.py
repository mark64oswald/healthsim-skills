"""Generation framework for MemberSim.

Re-exports healthsim-core generation infrastructure and provides
member-specific cohort generation.
"""

from healthsim.generation import (
    AgeDistribution,
    NormalDistribution,
    SeedManager,
    UniformDistribution,
    WeightedChoice,
)

from membersim.generation.cohort import (
    CohortConstraints,
    CohortGenerator,
    CohortProgress,
    MemberCohortConstraints,
    MemberCohortGenerator,
)

__all__ = [
    # Re-exported from healthsim-core
    "WeightedChoice",
    "UniformDistribution",
    "NormalDistribution",
    "AgeDistribution",
    "SeedManager",
    # Member-specific
    "MemberCohortConstraints",
    "MemberCohortGenerator",
    # Aliases for backward compatibility
    "CohortConstraints",
    "CohortProgress",
    "CohortGenerator",
]
