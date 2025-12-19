"""MemberSim - Synthetic health plan member data generation."""

from membersim.claims.claim import Claim, ClaimLine
from membersim.claims.payment import LinePayment, Payment
from membersim.core.accumulator import Accumulator
from membersim.core.member import Member, MemberGenerator
from membersim.core.plan import SAMPLE_PLANS, Plan
from membersim.core.provider import Provider
from membersim.core.subscriber import Subscriber
from membersim.dimensional import MemberSimDimensionalTransformer
from membersim.generation import (
    AgeDistribution,
    CohortConstraints,
    CohortGenerator,
    CohortProgress,
    NormalDistribution,
    SeedManager,
    UniformDistribution,
    WeightedChoice,
)
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

__version__ = "0.1.0"

__all__ = [
    # Core models
    "Member",
    "MemberGenerator",
    "Subscriber",
    "Plan",
    "SAMPLE_PLANS",
    "Provider",
    "Accumulator",
    # Claims
    "Claim",
    "ClaimLine",
    "Payment",
    "LinePayment",
    # Dimensional
    "MemberSimDimensionalTransformer",
    # Generation
    "WeightedChoice",
    "UniformDistribution",
    "NormalDistribution",
    "AgeDistribution",
    "SeedManager",
    "CohortConstraints",
    "CohortProgress",
    "CohortGenerator",
    # Scenarios
    "ScenarioDefinition",
    "ScenarioLibrary",
    "ScenarioEngine",
    "TimelineEvent",
    "MemberTimeline",
    "create_default_engine",
    "register_builtin_scenarios",
    "BUILTIN_SCENARIOS",
]
