import random
from typing import Any


def roulette_selection(
    population: list, fitnesses: list[float], rng: random.Random
) -> Any:
    """
    Roulette wheel selection: P(i) = f_i / sum(f).

    Requires fitness >= 0. If every fitness is 0, picks uniformly at random.

    Args:
        population: List of individuals
        fitnesses: Fitness of each individual (same order as population)
        rng: Random number generator

    Returns:
        The selected individual (not a copy)
    """
    # Step 1: Total size of the wheel
    total = sum(fitnesses)
    if total == 0:
        return rng.choice(population)

    # Step 2: Spin the wheel, then walk along the arcs until the spin is covered
    spin = rng.uniform(0, total)
    accumulated = 0.0
    for individual, fitness in zip(population, fitnesses):
        accumulated += fitness
        if accumulated >= spin:
            return individual

    # Step 3: Floating point safety net (accumulated may end slightly below spin)
    return population[-1]


def tournament_selection(
    population: list, fitnesses: list[float], rng: random.Random, k: int = 3
) -> Any:
    """
    Tournament selection: pick `k` random individuals, return the fittest.

    A larger `k` means a stronger selection pressure. Works with any fitness
    scale (negative values allowed).

    Args:
        population: List of individuals
        fitnesses: Fitness of each individual (same order as population)
        rng: Random number generator
        k: Tournament size (must be <= len(population))

    Returns:
        The selected individual (not a copy)
    """
    contestants = rng.sample(range(len(population)), k)
    winner = max(contestants, key=lambda i: fitnesses[i])
    return population[winner]
