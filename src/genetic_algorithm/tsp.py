import itertools
import math
import random
from collections.abc import Callable

from src.genetic_algorithm.crossover import order_crossover
from src.genetic_algorithm.genetic_algorithm import GAConfig, run_ga
from src.genetic_algorithm.mutation import swap_mutation
from src.utils.ga_problem import GAProblem


class TSP(GAProblem):
    """
    Travelling salesman problem: shortest closed tour visiting every city once.

    Chromosome: permutation of 0..n-1 (the order the cities are visited).
    Fitness: 1 / tour length (TSP is a minimisation, the GA maximises).
    Operators: order crossover (OX); mutation is swap by default
    (`rate` is the probability of mutating the whole tour).
    """

    def __init__(
        self,
        cities: list[tuple[float, float]],
        mutation: Callable[[list, float, random.Random], list] = swap_mutation,
    ):
        self.cities = cities
        self.mutation = mutation
        # Pre-compute distances: they are looked up many times per generation
        self._dist = [[math.dist(a, b) for b in cities] for a in cities]

    @property
    def size(self) -> int:
        """Number of cities (= chromosome length)."""
        return len(self.cities)

    def tour_length(self, tour: list[int]) -> float:
        """Length of the closed tour (it returns to its first city)."""
        return sum(
            self._dist[tour[i]][tour[(i + 1) % self.size]] for i in range(self.size)
        )

    def random_individual(self, rng: random.Random) -> list[int]:
        tour = list(range(self.size))
        rng.shuffle(tour)
        return tour

    def fitness(self, individual: list[int]) -> float:
        length = self.tour_length(individual)
        return 1.0 / length if length > 0 else math.inf

    def crossover(
        self, parent1: list[int], parent2: list[int], rng: random.Random
    ) -> tuple[list[int], list[int]]:
        return order_crossover(parent1, parent2, rng)

    def mutate(
        self, individual: list[int], rate: float, rng: random.Random
    ) -> list[int]:
        return self.mutation(individual, rate, rng)

    def brute_force(self) -> tuple[list[int], float]:
        """
        Try every tour with city 0 fixed: (n-1)! tours (only for small n).

        Returns:
            (shortest tour, its length)
        """
        best_tour = min(
            ([0, *rest] for rest in itertools.permutations(range(1, self.size))),
            key=self.tour_length,
        )
        return best_tour, self.tour_length(best_tour)


def random_cities(size: int, rng: random.Random) -> list[tuple[float, float]]:
    """
    Build `size` random cities on a 200 x 200 plane.

    Args:
        size: Number of cities
        rng: Random number generator

    Returns:
        List of (x, y) coordinates
    """
    return [(rng.randint(0, 200), rng.randint(0, 200)) for _ in range(size)]


def main():
    problem = TSP(random_cities(10, random.Random(0)))
    config = GAConfig(
        population_size=100,
        generations=300,
        crossover_rate=0.9,
        mutation_rate=0.2,
        elite_size=2,
    )

    _, optimum = problem.brute_force()
    results = [run_ga(problem, config, seed=s) for s in range(20)]
    lengths = [problem.tour_length(r.best) for r in results]
    hits = sum(abs(length - optimum) < 0.01 for length in lengths)
    print("best length of each run:", [round(length, 2) for length in lengths])
    print(f"optimum (brute force): {optimum:.2f}, GA hit it in {hits}/20 runs")

    best = min(results, key=lambda r: problem.tour_length(r.best))
    print("best tour:", best.best, "length:", round(problem.tour_length(best.best), 2))


if __name__ == "__main__":
    main()
