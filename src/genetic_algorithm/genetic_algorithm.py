import math
import random
from collections.abc import Callable
from dataclasses import dataclass
from typing import Any

from src.genetic_algorithm.selection import tournament_selection
from src.utils.ga_problem import GAProblem, GAResult

# selection(population, fitnesses, rng) -> one individual
Selection = Callable[[list, list[float], random.Random], Any]


@dataclass
class GAConfig:
    """Parameters of a GA run (see notebook 8.4.8)."""

    population_size: int = 100
    generations: int = 100
    crossover_rate: float = 0.8  # Pc: probability that two parents are crossed
    mutation_rate: float = 0.05  # Pm: passed to `GAProblem.mutate`
    elite_size: int = 1  # best individuals copied unchanged to the next generation
    selection: Selection = tournament_selection

    def __post_init__(self):
        if self.population_size < 2:
            raise ValueError("population_size must be >= 2")
        if not 0 <= self.elite_size <= self.population_size:
            raise ValueError("elite_size must be in [0, population_size]")


def init_population(
    problem: GAProblem, population_size: int, rng: random.Random
) -> list:
    """
    Create the initial population P(0)

    Args:
        problem: Problem that knows how to build a random valid individual
        population_size: Number of individuals N
        rng: Random number generator

    Returns:
        List of N random individuals
    """
    return [problem.random_individual(rng) for _ in range(population_size)]


def run_ga(
    problem: GAProblem, config: GAConfig | None = None, seed: int | None = None
) -> GAResult:
    """
    Generational Genetic Algorithm (notebook 8.3)

    Args:
        problem: Problem to solve (encoding, fitness and genetic operators)
        config: GA parameters (defaults to `GAConfig()`)
        seed: Seed of the random generator (None = not reproducible)

    Returns:
        GAResult with the best individual found and the per-generation history
    """
    config = config or GAConfig()
    rng = random.Random(seed)

    # Step 1: Create the initial population P(0) of random individuals
    population = init_population(problem, config.population_size, rng)

    best: Any = None
    best_fitness = -math.inf
    best_history: list[float] = []
    avg_history: list[float] = []
    evaluations = 0

    for generation in range(config.generations + 1):
        # Step 2: Evaluate every individual of P(t) and update statistics
        fitnesses = [problem.fitness(individual) for individual in population]
        evaluations += len(population)

        top = max(range(len(population)), key=lambda i: fitnesses[i])
        if fitnesses[top] > best_fitness:
            best, best_fitness = population[top], fitnesses[top]
        best_history.append(fitnesses[top])
        avg_history.append(sum(fitnesses) / len(fitnesses))

        # Step 3: Stop after the last generation (no need to breed one more)
        if generation == config.generations:
            break

        # Step 4: Elitism - copy the best individuals unchanged
        ranked = sorted(
            range(len(population)), key=lambda i: fitnesses[i], reverse=True
        )
        next_population = [population[i] for i in ranked[: config.elite_size]]

        # Step 5: Fill the rest with children
        while len(next_population) < config.population_size:
            # 5a: Selection - choose 2 parents according to fitness
            parent1 = config.selection(population, fitnesses, rng)
            parent2 = config.selection(population, fitnesses, rng)

            # 5b: Crossover with probability Pc (otherwise children = parents)
            if rng.random() < config.crossover_rate:
                child1, child2 = problem.crossover(parent1, parent2, rng)
            else:
                child1, child2 = parent1, parent2

            # 5c: Mutation
            next_population.append(problem.mutate(child1, config.mutation_rate, rng))
            next_population.append(problem.mutate(child2, config.mutation_rate, rng))

        # Step 6: P(t+1) replaces P(t) (trim in case of an odd population size)
        population = next_population[: config.population_size]

    return GAResult(best, best_fitness, best_history, avg_history, evaluations)
