"""Data generation framework.

This module provides base classes and utilities for generating
synthetic data with reproducibility support.
"""

from healthsim.generation.base import BaseGenerator, PersonGenerator
from healthsim.generation.cohort import (
    CohortConstraints,
    CohortGenerator,
    CohortProgress,
)
from healthsim.generation.distributions import (
    AgeDistribution,
    NormalDistribution,
    UniformDistribution,
    WeightedChoice,
)
from healthsim.generation.reproducibility import SeedManager

__all__ = [
    # Generators
    "BaseGenerator",
    "PersonGenerator",
    "CohortGenerator",
    "CohortConstraints",
    "CohortProgress",
    # Distributions
    "WeightedChoice",
    "NormalDistribution",
    "UniformDistribution",
    "AgeDistribution",
    # Reproducibility
    "SeedManager",
]
