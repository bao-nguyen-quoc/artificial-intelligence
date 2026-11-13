import itertools
import random

from src.genetic_algorithm.crossover import one_point_crossover
from src.genetic_algorithm.genetic_algorithm import GAConfig, run_ga
from src.genetic_algorithm.mutation import bit_flip_mutation
from src.utils.ga_problem import GAProblem


class Knapsack(GAProblem):
    """
    0/1 knapsack: maximise the total value without exceeding the capacity.

    Chromosome: bit string of length n, bit i = 1 means item i is in the bag.
    Fitness: total value, or 0 when the bag is overloaded ("death penalty",
    notebook 8.4.3).
    Operators: one-point crossover, bit-flip mutation (`rate` is per bit).
    """

    def __init__(self, weights: list[int], values: list[int], capacity: int):
        if len(weights) != len(values):
            raise ValueError("weights and values must have the same length")
        self.weights = weights
        self.values = values
        self.capacity = capacity

    @property
    def size(self) -> int:
        """Number of items (= chromosome length)."""
        return len(self.weights)

    def total_weight(self, chromosome: list[int]) -> int:
        return sum(c * w for c, w in zip(chromosome, self.weights))

    def total_value(self, chromosome: list[int]) -> int:
        return sum(c * v for c, v in zip(chromosome, self.values))

    def selected_items(self, chromosome: list[int]) -> list[int]:
        """Return the (1-based) numbers of the items in the bag."""
        return [i + 1 for i, c in enumerate(chromosome) if c]

    def random_individual(self, rng: random.Random) -> list[int]:
        return [rng.randint(0, 1) for _ in range(self.size)]

    def fitness(self, individual: list[int]) -> float:
        if self.total_weight(individual) > self.capacity:
            return 0
        return self.total_value(individual)

    def crossover(
        self, parent1: list[int], parent2: list[int], rng: random.Random
    ) -> tuple[list[int], list[int]]:
        return one_point_crossover(parent1, parent2, rng)

    def mutate(
        self, individual: list[int], rate: float, rng: random.Random
    ) -> list[int]:
        return bit_flip_mutation(individual, rate, rng)

    def brute_force(self) -> tuple[list[int], int]:
        """
        Check all 2^n combinations (only for small n, used to verify the GA).

        Returns:
            (best chromosome, best value)
        """
        best = max(
            itertools.product([0, 1], repeat=self.size),
            key=lambda c: self.fitness(list(c)),
        )
        return list(best), self.total_value(list(best))


def random_knapsack(size: int, rng: random.Random) -> Knapsack:
    """
    Build a random instance: `size` items, capacity = 1/3 of the total weight.

    Args:
        size: Number of items
        rng: Random number generator

    Returns:
        A random Knapsack problem
    """
    weights = [rng.randint(1, 20) for _ in range(size)]
    values = [rng.randint(1, 50) for _ in range(size)]
    return Knapsack(weights, values, capacity=sum(weights) // 3)


def main():
    rng = random.Random(0)
    problem = random_knapsack(15, rng)
    config = GAConfig(
        population_size=30,
        generations=50,
        crossover_rate=0.8,
        mutation_rate=1 / problem.size,
        elite_size=1,
    )

    result = run_ga(problem, config, seed=42)
    for gen, (best, avg) in enumerate(zip(result.best_history, result.avg_history)):
        print(f"gen {gen:2d} best={best:3.0f} avg={avg:6.1f}")
    print("best:", result.best, "fitness:", result.best_fitness)
    print("items:", problem.selected_items(result.best))
    print("weight:", problem.total_weight(result.best), "/", problem.capacity)

    _, optimum = problem.brute_force()
    hits = sum(
        run_ga(problem, config, seed=s).best_fitness == optimum for s in range(100)
    )
    print(f"optimum (brute force): {optimum}, GA hit it in {hits}/100 runs")


if __name__ == "__main__":
    main()
