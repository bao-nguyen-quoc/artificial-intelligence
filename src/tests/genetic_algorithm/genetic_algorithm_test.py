import itertools
import random

import pytest

from src.genetic_algorithm.genetic_algorithm import GAConfig, init_population, run_ga
from src.genetic_algorithm.knapsack import Knapsack
from src.genetic_algorithm.selection import roulette_selection
from src.utils.ga_problem import GAProblem


class OneMax(GAProblem):
    """Toy problem: maximise the number of 1 bits (also checks the engine contract)."""

    def __init__(self, size: int = 20):
        self.size = size
        self.evaluated: list = []

    def random_individual(self, rng):
        return [rng.randint(0, 1) for _ in range(self.size)]

    def fitness(self, individual):
        self.evaluated.append(individual)
        return sum(individual)

    def crossover(self, parent1, parent2, rng):
        cut = rng.randint(1, self.size - 1)
        return parent1[:cut] + parent2[cut:], parent2[:cut] + parent1[cut:]

    def mutate(self, individual, rate, rng):
        return [1 - g if rng.random() < rate else g for g in individual]


class TestInitPopulation:
    """Tests for the initial population."""

    def test_size_and_individuals(self):
        """N individuals, each one built by the problem."""
        population = init_population(OneMax(8), 15, random.Random(0))

        assert len(population) == 15
        assert all(len(individual) == 8 for individual in population)
        assert all(set(individual) <= {0, 1} for individual in population)

    def test_same_seed_same_population(self):
        assert init_population(OneMax(), 10, random.Random(3)) == init_population(
            OneMax(), 10, random.Random(3)
        )

    def test_individuals_are_independent_objects(self):
        population = init_population(OneMax(), 5, random.Random(0))

        assert len({id(individual) for individual in population}) == 5


class TestRunGA:
    """Tests for the generic GA engine."""

    def test_solves_one_max(self):
        """The GA finds the all-ones string."""
        config = GAConfig(population_size=30, generations=50, mutation_rate=0.02)
        result = run_ga(OneMax(), config, seed=0)

        assert result.best == [1] * 20
        assert result.best_fitness == 20

    def test_same_seed_same_result(self):
        """A run is reproducible from its seed."""
        config = GAConfig(population_size=20, generations=15)
        r1 = run_ga(OneMax(), config, seed=7)
        r2 = run_ga(OneMax(), config, seed=7)

        assert r1.best == r2.best
        assert r1.best_history == r2.best_history
        assert r1.avg_history == r2.avg_history

    def test_history_and_evaluation_count(self):
        """One history entry per generation (including generation 0)."""
        config = GAConfig(population_size=10, generations=5)
        problem = OneMax()
        result = run_ga(problem, config, seed=0)

        assert len(result.best_history) == 6
        assert len(result.avg_history) == 6
        assert result.evaluations == 60
        assert len(problem.evaluated) == 60

    def test_elitism_never_lowers_best_fitness(self):
        """With elitism the best fitness is non-decreasing across generations."""
        config = GAConfig(population_size=20, generations=40, elite_size=1)
        history = run_ga(OneMax(), config, seed=3).best_history

        assert all(a <= b for a, b in itertools.pairwise(history))

    def test_best_is_best_of_whole_run(self):
        """Even without elitism, `best` is the best individual ever evaluated."""
        config = GAConfig(population_size=10, generations=20, elite_size=0)
        problem = OneMax()
        result = run_ga(problem, config, seed=1)

        assert result.best_fitness == max(sum(i) for i in problem.evaluated)
        assert result.best_fitness == max(result.best_history)

    def test_elites_are_copied_unchanged(self):
        """Mutation rate 1 flips every child, but the elite survives intact."""
        config = GAConfig(
            population_size=10,
            generations=1,
            crossover_rate=0.0,
            mutation_rate=1.0,
            elite_size=1,
        )
        problem = OneMax()
        run_ga(problem, config, seed=0)
        first_gen, second_gen = problem.evaluated[:10], problem.evaluated[10:]
        best = max(first_gen, key=sum)

        assert best in second_gen

    def test_odd_population_size_is_kept(self):
        """Children come in pairs but the population size stays exact."""
        config = GAConfig(population_size=7, generations=3)
        problem = OneMax()
        run_ga(problem, config, seed=0)

        assert len(problem.evaluated) == 7 * 4

    def test_works_with_roulette_selection(self):
        """Selection operator is pluggable through the config."""
        config = GAConfig(
            population_size=30, generations=50, selection=roulette_selection
        )
        result = run_ga(OneMax(), config, seed=0)

        assert result.best_fitness >= 18

    def test_zero_generations_only_evaluates_initial_population(self):
        config = GAConfig(population_size=5, generations=0)
        result = run_ga(OneMax(), config, seed=0)

        assert result.evaluations == 5
        assert len(result.best_history) == 1

    def test_default_config(self):
        result = run_ga(OneMax(), seed=0)

        assert len(result.best_history) == GAConfig().generations + 1

    def test_individuals_are_not_shared_between_runs(self):
        """Operators must not mutate individuals that are still in the population."""
        problem = Knapsack([1, 2, 3], [4, 5, 6], 4)
        before = random.Random(0)
        initial = [problem.random_individual(before) for _ in range(6)]
        config = GAConfig(population_size=6, generations=10, mutation_rate=0.5)
        run_ga(problem, config, seed=0)

        again = random.Random(0)
        assert initial == [problem.random_individual(again) for _ in range(6)]


class TestGAConfig:
    """Tests for config validation."""

    def test_population_too_small(self):
        with pytest.raises(ValueError):
            GAConfig(population_size=1)

    def test_elite_larger_than_population(self):
        with pytest.raises(ValueError):
            GAConfig(population_size=5, elite_size=6)

    def test_negative_elite(self):
        with pytest.raises(ValueError):
            GAConfig(elite_size=-1)
