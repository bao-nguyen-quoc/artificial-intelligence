import random
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import Any


class GAProblem(ABC):
    """
    Interface for a problem that can be solved by the genetic algorithm.

    The GA engine only knows about populations, selection and generations.
    Everything that depends on the problem (encoding, fitness, genetic
    operators) is provided by an implementation of this interface.

    Convention: fitness is MAXIMISED and must be >= 0 (roulette selection needs it).
    Individuals must be treated as immutable: `crossover` and `mutate` return NEW
    individuals and never modify their arguments.
    All randomness must come from the `rng` passed in, so a run is reproducible
    from its seed.
    """

    @abstractmethod
    def random_individual(self, rng: random.Random) -> Any:
        """Return a random (valid) individual."""

    @abstractmethod
    def fitness(self, individual: Any) -> float:
        """Return the fitness of `individual` (higher is better, never negative)."""

    @abstractmethod
    def crossover(
        self, parent1: Any, parent2: Any, rng: random.Random
    ) -> tuple[Any, Any]:
        """Return two children made from the genes of the two parents."""

    @abstractmethod
    def mutate(self, individual: Any, rate: float, rng: random.Random) -> Any:
        """
        Return a (possibly) mutated copy of `individual`.

        The meaning of `rate` depends on the encoding: probability for EACH gene
        (bit strings) or probability for the WHOLE individual (permutations).
        """


@dataclass
class GAResult:
    """Result returned by `run_ga`."""

    best: Any  # best individual found during the whole run
    best_fitness: float  # fitness of `best`
    best_history: list[float] = field(
        default_factory=list
    )  # best fitness per generation
    avg_history: list[float] = field(
        default_factory=list
    )  # average fitness per generation
    evaluations: int = 0  # number of fitness evaluations (used to compare budgets)
