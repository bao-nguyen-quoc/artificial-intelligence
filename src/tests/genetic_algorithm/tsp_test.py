import itertools
import math
import random

import pytest

from src.genetic_algorithm.genetic_algorithm import GAConfig, run_ga
from src.genetic_algorithm.mutation import inversion_mutation
from src.genetic_algorithm.tsp import TSP, random_cities

# ──────────────────────────────────────────────────────────────────────
# Preset data: 10 cities, Euclidean distance, closed tour
# ──────────────────────────────────────────────────────────────────────
NOTEBOOK_CITIES = [
    (60, 200),
    (180, 200),
    (80, 180),
    (140, 180),
    (20, 160),
    (100, 160),
    (200, 160),
    (140, 140),
    (40, 120),
    (100, 120),
]
# Shortest tour (found by brute force); rotations / reversals have the same length
NOTEBOOK_OPTIMUM = 459.99
OPTIMAL_TOUR = [0, 2, 5, 3, 1, 6, 7, 9, 8, 4]

# Parameters of the exercise (selection = tournament, k = 3)
NOTEBOOK_CONFIG = GAConfig(
    population_size=100,
    generations=300,
    crossover_rate=0.9,
    mutation_rate=0.2,
    elite_size=2,
)


class TestTSPProblem:
    """Tests for the TSP encoding and fitness."""

    def test_square_tour_length(self):
        """The tour is closed: it returns to the first city."""
        problem = TSP([(0, 0), (0, 1), (1, 1), (1, 0)])

        assert problem.tour_length([0, 1, 2, 3]) == pytest.approx(4.0)
        assert problem.tour_length([0, 2, 1, 3]) == pytest.approx(2 + 2 * math.sqrt(2))

    def test_tour_length_is_rotation_and_reversal_invariant(self):
        problem = TSP(NOTEBOOK_CITIES)
        length = problem.tour_length(OPTIMAL_TOUR)

        assert problem.tour_length(
            OPTIMAL_TOUR[3:] + OPTIMAL_TOUR[:3]
        ) == pytest.approx(length)
        assert problem.tour_length(OPTIMAL_TOUR[::-1]) == pytest.approx(length)

    def test_notebook_optimal_tour_length(self):
        assert TSP(NOTEBOOK_CITIES).tour_length(OPTIMAL_TOUR) == pytest.approx(
            NOTEBOOK_OPTIMUM, abs=0.01
        )

    def test_fitness_is_inverse_of_length(self):
        """Shorter tour -> higher fitness (minimisation turned into maximisation)."""
        problem = TSP(NOTEBOOK_CITIES)
        short, long = OPTIMAL_TOUR, list(range(10))

        assert problem.fitness(short) == pytest.approx(1 / problem.tour_length(short))
        assert problem.fitness(short) > problem.fitness(long)

    def test_random_cities(self):
        """Random cities: right count, reproducible, inside the 200 x 200 plane."""
        cities = random_cities(10, random.Random(5))

        assert len(cities) == 10
        assert cities == random_cities(10, random.Random(5))
        assert all(0 <= x <= 200 and 0 <= y <= 200 for x, y in cities)

    def test_random_individuals_are_valid_permutations(self):
        problem = TSP(NOTEBOOK_CITIES)
        rng = random.Random(0)
        for _ in range(100):
            assert sorted(problem.random_individual(rng)) == list(range(10))

    def test_operators_keep_permutations_valid(self):
        """Every offspring is a valid permutation of 0..N-1."""
        problem = TSP(NOTEBOOK_CITIES)
        rng = random.Random(0)
        for _ in range(200):
            p1, p2 = problem.random_individual(rng), problem.random_individual(rng)
            for child in problem.crossover(p1, p2, rng):
                assert sorted(problem.mutate(child, 1.0, rng)) == list(range(10))

    def test_brute_force_matches_known_optimum(self):
        """(n-1)! = 362 880 tours with city 0 fixed."""
        tour, length = TSP(NOTEBOOK_CITIES).brute_force()

        assert length == pytest.approx(NOTEBOOK_OPTIMUM, abs=0.01)
        assert tour[0] == 0
        assert sorted(tour) == list(range(10))


class TestTSPGA:
    """The GA solves the 10-city exercise."""

    def test_never_shorter_than_optimum(self):
        """A shorter result would mean a bug in length or validity."""
        problem = TSP(NOTEBOOK_CITIES)
        for seed in range(5):
            result = run_ga(problem, NOTEBOOK_CONFIG, seed=seed)
            assert sorted(result.best) == list(range(10))
            assert problem.tour_length(result.best) >= NOTEBOOK_OPTIMUM - 0.01

    def test_hits_optimum_at_least_15_of_20_runs(self):
        """Requirement of the exercise with POP=100, GENS=300, PC=0.9, PM=0.2, K=3, ELITE=2."""
        problem = TSP(NOTEBOOK_CITIES)
        lengths = [
            problem.tour_length(run_ga(problem, NOTEBOOK_CONFIG, seed=s).best)
            for s in range(20)
        ]
        hits = sum(abs(length - NOTEBOOK_OPTIMUM) < 0.01 for length in lengths)

        assert hits >= 15

    def test_convergence_curve_is_non_increasing_in_length(self):
        """With elitism the best tour length never gets worse."""
        problem = TSP(NOTEBOOK_CITIES)
        history = run_ga(problem, NOTEBOOK_CONFIG, seed=0).best_history
        lengths = [1 / f for f in history]

        assert len(history) == NOTEBOOK_CONFIG.generations + 1
        assert all(a >= b - 1e-9 for a, b in itertools.pairwise(lengths))
        assert lengths[-1] < lengths[0]

    def test_inversion_mutation_is_pluggable(self):
        problem = TSP(NOTEBOOK_CITIES, mutation=inversion_mutation)
        result = run_ga(problem, NOTEBOOK_CONFIG, seed=0)

        assert sorted(result.best) == list(range(10))
        assert problem.tour_length(result.best) < 520

    def test_beats_random_search_with_same_budget(self):
        """Same number of fitness evaluations: GA is better than random permutations."""
        problem = TSP(NOTEBOOK_CITIES)
        config = GAConfig(
            population_size=50,
            generations=100,
            crossover_rate=0.9,
            mutation_rate=0.2,
            elite_size=2,
        )
        ga = run_ga(problem, config, seed=0)

        rng = random.Random(0)
        random_best = min(
            problem.tour_length(problem.random_individual(rng))
            for _ in range(ga.evaluations)
        )

        assert problem.tour_length(ga.best) <= random_best
