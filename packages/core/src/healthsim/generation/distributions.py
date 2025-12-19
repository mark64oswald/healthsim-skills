"""Statistical distributions for data generation.

Provides distribution classes for generating values according
to various statistical distributions.
"""

import random
from abc import ABC, abstractmethod
from typing import Any, Generic, TypeVar

from pydantic import BaseModel

T = TypeVar("T")


class WeightedChoice(BaseModel, Generic[T]):
    """Weighted random selection from options.

    Allows selecting from a list of options where each option
    has an associated weight/probability.

    Attributes:
        options: List of (option, weight) tuples

    Example:
        >>> choices = WeightedChoice(options=[
        ...     ("common", 0.7),
        ...     ("uncommon", 0.2),
        ...     ("rare", 0.1)
        ... ])
        >>> # "common" will be selected ~70% of the time
        >>> choices.select()
        'common'
    """

    options: list[tuple[Any, float]]

    def select(self, rng: random.Random | None = None) -> Any:
        """Select an option based on weights.

        Args:
            rng: Random number generator (for reproducibility)

        Returns:
            Selected option
        """
        if not self.options:
            raise ValueError("No options to select from")

        if rng is None:
            rng = random.Random()

        items = [opt[0] for opt in self.options]
        weights = [opt[1] for opt in self.options]

        return rng.choices(items, weights=weights, k=1)[0]

    def select_multiple(
        self,
        count: int,
        rng: random.Random | None = None,
        unique: bool = False,
    ) -> list[Any]:
        """Select multiple options.

        Args:
            count: Number of options to select
            rng: Random number generator
            unique: If True, each option can only be selected once

        Returns:
            List of selected options
        """
        if not self.options:
            raise ValueError("No options to select from")

        if rng is None:
            rng = random.Random()

        items = [opt[0] for opt in self.options]
        weights = [opt[1] for opt in self.options]

        if unique:
            if count > len(items):
                raise ValueError(f"Cannot select {count} unique items from {len(items)} options")

            selected = []
            remaining_items = list(items)
            remaining_weights = list(weights)

            for _ in range(count):
                choice = rng.choices(remaining_items, weights=remaining_weights, k=1)[0]
                selected.append(choice)
                idx = remaining_items.index(choice)
                remaining_items.pop(idx)
                remaining_weights.pop(idx)

            return selected
        else:
            return rng.choices(items, weights=weights, k=count)


class Distribution(ABC):
    """Abstract base class for statistical distributions."""

    @abstractmethod
    def sample(self, rng: random.Random | None = None) -> float:
        """Sample a value from the distribution.

        Args:
            rng: Random number generator

        Returns:
            Sampled value
        """
        ...


class NormalDistribution(Distribution, BaseModel):
    """Normal (Gaussian) distribution.

    Attributes:
        mean: Mean of the distribution
        std_dev: Standard deviation

    Example:
        >>> dist = NormalDistribution(mean=100, std_dev=15)
        >>> value = dist.sample()  # ~100 +/- 15
    """

    mean: float
    std_dev: float

    def sample(self, rng: random.Random | None = None) -> float:
        """Sample from the normal distribution.

        Args:
            rng: Random number generator

        Returns:
            Sampled value
        """
        if rng is None:
            rng = random.Random()
        return rng.gauss(self.mean, self.std_dev)

    def sample_int(self, rng: random.Random | None = None) -> int:
        """Sample and round to integer.

        Args:
            rng: Random number generator

        Returns:
            Sampled integer value
        """
        return round(self.sample(rng))

    def sample_bounded(
        self,
        min_val: float | None = None,
        max_val: float | None = None,
        rng: random.Random | None = None,
    ) -> float:
        """Sample with bounds, re-sampling if outside range.

        Args:
            min_val: Minimum allowed value
            max_val: Maximum allowed value
            rng: Random number generator

        Returns:
            Sampled value within bounds
        """
        max_attempts = 1000
        for _ in range(max_attempts):
            value = self.sample(rng)
            if min_val is not None and value < min_val:
                continue
            if max_val is not None and value > max_val:
                continue
            return value

        # Fallback: clamp to bounds
        value = self.sample(rng)
        if min_val is not None and value < min_val:
            return min_val
        if max_val is not None and value > max_val:
            return max_val
        return value


class UniformDistribution(Distribution, BaseModel):
    """Uniform distribution between min and max.

    Attributes:
        min_val: Minimum value (inclusive)
        max_val: Maximum value (inclusive)

    Example:
        >>> dist = UniformDistribution(min_val=0, max_val=100)
        >>> value = dist.sample()  # 0 to 100 with equal probability
    """

    min_val: float
    max_val: float

    def sample(self, rng: random.Random | None = None) -> float:
        """Sample from the uniform distribution.

        Args:
            rng: Random number generator

        Returns:
            Sampled value
        """
        if rng is None:
            rng = random.Random()
        return rng.uniform(self.min_val, self.max_val)

    def sample_int(self, rng: random.Random | None = None) -> int:
        """Sample and return integer.

        Args:
            rng: Random number generator

        Returns:
            Sampled integer value
        """
        if rng is None:
            rng = random.Random()
        return rng.randint(int(self.min_val), int(self.max_val))


class AgeDistribution:
    """Age distribution for population generation.

    Provides weighted random age selection based on
    configurable age bands.
    """

    def __init__(self, bands: list[tuple[int, int, float]] | None = None):
        """Initialize age distribution.

        Args:
            bands: List of (min_age, max_age, weight) tuples
        """
        if bands is None:
            # Default adult distribution
            self.bands = [
                (18, 30, 0.20),
                (31, 45, 0.25),
                (46, 60, 0.25),
                (61, 75, 0.20),
                (76, 90, 0.10),
            ]
        else:
            self.bands = bands
        self._rng = random.Random()

    def seed(self, seed: int) -> None:
        """Set random seed for reproducibility."""
        self._rng = random.Random(seed)

    def sample(self) -> int:
        """Sample an age from the distribution."""
        # Weighted selection of band
        weights = [band[2] for band in self.bands]
        band = self._rng.choices(self.bands, weights=weights, k=1)[0]

        # Random age within band
        return self._rng.randint(band[0], band[1])

    def sample_many(self, count: int) -> list[int]:
        """Sample multiple ages."""
        return [self.sample() for _ in range(count)]

    @classmethod
    def pediatric(cls) -> "AgeDistribution":
        """Create pediatric age distribution (0-17)."""
        return cls(
            bands=[
                (0, 2, 0.15),
                (3, 5, 0.15),
                (6, 12, 0.35),
                (13, 17, 0.35),
            ]
        )

    @classmethod
    def adult(cls) -> "AgeDistribution":
        """Create adult age distribution (18-90)."""
        return cls()  # Uses default

    @classmethod
    def senior(cls) -> "AgeDistribution":
        """Create senior age distribution (65+)."""
        return cls(
            bands=[
                (65, 70, 0.30),
                (71, 75, 0.25),
                (76, 80, 0.20),
                (81, 85, 0.15),
                (86, 95, 0.10),
            ]
        )
