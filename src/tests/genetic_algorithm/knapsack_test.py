import random

import pytest

from src.genetic_algorithm.genetic_algorithm import GAConfig, run_ga
from src.genetic_algorithm.knapsack import Knapsack, random_knapsack
from src.genetic_algorithm.selection import roulette_selection, tournament_selection

# ──────────────────────────────────────────────────────────────────────
# Preset data: example of notebook 8.7 (6 items, capacity 15)
# Optimum = items 2, 3, 4, 6 (weight 15, value 145)
# ──────────────────────────────────────────────────────────────────────
NOTEBOOK_WEIGHTS = [5, 4, 6, 3, 7, 2]
NOTEBOOK_VALUES = [10, 40, 30, 50, 35, 25]
NOTEBOOK_CAPACITY = 15
NOTEBOOK_OPTIMUM = 145

# Parameters of notebook 8.7
NOTEBOOK_CONFIG = GAConfig(
    population_size=20,
    generations=30,
    crossover_rate=0.8,
    mutation_rate=0.05,
    elite_size=1,
    selection=roulette_selection,
)


def notebook_knapsack() -> Knapsack:
    """Build the 6-item example of notebook 8.7."""
    return Knapsack(NOTEBOOK_WEIGHTS, NOTEBOOK_VALUES, NOTEBOOK_CAPACITY)


class TestKnapsackProblem:
    """Tests for the knapsack encoding and fitness (notebook 8.7.2 - 8.7.3)."""

    def test_decode_chromosome(self):
        """110101 -> items 1, 2, 4, 6 with weight 14 and value 125."""
        problem = notebook_knapsack()
        chromosome = [1, 1, 0, 1, 0, 1]

        assert problem.selected_items(chromosome) == [1, 2, 4, 6]
        assert problem.total_weight(chromosome) == 14
        assert problem.total_value(chromosome) == 125

    @pytest.mark.parametrize(
        "chromosome, expected",
        [
            ([1, 0, 1, 1, 0, 0], 90),  # A
            ([0, 1, 1, 0, 1, 0], 0),  # B: weight 17 > 15, rejected
            ([1, 1, 0, 1, 0, 1], 125),  # C
            ([0, 1, 0, 1, 0, 1], 115),  # D
            ([1, 0, 1, 1, 0, 1], 0),  # offspring of the crossover example (16 > 15)
            ([0, 0, 0, 0, 0, 0], 0),
        ],
    )
    def test_fitness_table_of_notebook(self, chromosome, expected):
        assert notebook_knapsack().fitness(chromosome) == expected

    def test_brute_force_finds_notebook_optimum(self):
        """Items 2, 3, 4, 6: weight 15, value 145."""
        chromosome, value = notebook_knapsack().brute_force()

        assert chromosome == [0, 1, 1, 1, 0, 1]
        assert value == NOTEBOOK_OPTIMUM

    def test_weights_and_values_must_match(self):
        with pytest.raises(ValueError):
            Knapsack([1, 2], [3], 5)

    def test_random_knapsack(self):
        """Random instance: right size, reproducible, capacity = 1/3 of total weight."""
        problem = random_knapsack(12, random.Random(5))
        again = random_knapsack(12, random.Random(5))

        assert problem.size == 12
        assert problem.capacity == sum(problem.weights) // 3
        assert (problem.weights, problem.values) == (again.weights, again.values)


class TestKnapsackGA:
    """The GA solves the example of notebook 8.7."""

    def test_finds_optimum_with_notebook_seed(self):
        """Notebook 8.7.9: seed 42 reaches 145 at generation 2 and keeps it."""
        problem = notebook_knapsack()
        result = run_ga(problem, NOTEBOOK_CONFIG, seed=42)

        assert result.best == [0, 1, 1, 1, 0, 1]
        assert result.best_fitness == NOTEBOOK_OPTIMUM
        assert result.best_history[0] == 125
        assert result.best_history[2:] == [145] * 29  # elitism: never drops

    def test_hit_rate_over_100_seeds(self):
        """Notebook 8.7.9: 97/100 runs find the optimum."""
        problem = notebook_knapsack()
        hits = sum(
            run_ga(problem, NOTEBOOK_CONFIG, seed=s).best_fitness == NOTEBOOK_OPTIMUM
            for s in range(100)
        )

        assert hits >= 90

    def test_best_individual_is_always_feasible(self):
        problem = notebook_knapsack()
        for seed in range(10):
            result = run_ga(problem, NOTEBOOK_CONFIG, seed=seed)
            assert problem.total_weight(result.best) <= problem.capacity

    def test_tournament_selection_also_works(self):
        problem = notebook_knapsack()
        config = GAConfig(
            population_size=20,
            generations=30,
            crossover_rate=0.8,
            mutation_rate=0.05,
            elite_size=1,
            selection=tournament_selection,
        )
        hits = sum(
            run_ga(problem, config, seed=s).best_fitness == NOTEBOOK_OPTIMUM
            for s in range(30)
        )

        assert hits >= 20

    def test_larger_instance_beats_greedy_floor_and_respects_capacity(self):
        """30 items: brute force (2^30) is too slow, the GA must still be feasible and good."""
        problem = random_knapsack(30, random.Random(0))
        weights, values = problem.weights, problem.values
        config = GAConfig(
            population_size=60,
            generations=100,
            crossover_rate=0.8,
            mutation_rate=1 / 30,
            elite_size=2,
        )
        result = run_ga(problem, config, seed=0)

        # Greedy by value/weight ratio is a decent baseline for this size
        remaining, greedy = problem.capacity, 0
        for w, v in sorted(
            zip(weights, values), key=lambda wv: wv[1] / wv[0], reverse=True
        ):
            if w <= remaining:
                remaining -= w
                greedy += v

        assert problem.total_weight(result.best) <= problem.capacity
        assert result.best_fitness >= 0.9 * greedy
