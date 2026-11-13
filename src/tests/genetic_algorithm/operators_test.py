import random
from collections import Counter

import pytest

from src.genetic_algorithm.crossover import one_point_crossover, order_crossover
from src.genetic_algorithm.mutation import (
    bit_flip_mutation,
    inversion_mutation,
    swap_mutation,
)
from src.genetic_algorithm.selection import roulette_selection, tournament_selection


class TestSelection:
    """Tests for roulette and tournament selection."""

    def test_roulette_never_picks_zero_fitness(self):
        """An individual with fitness 0 has an empty arc on the wheel."""
        rng = random.Random(0)
        population = ["A", "B", "C"]
        fitnesses = [90, 0, 125]
        picks = {roulette_selection(population, fitnesses, rng) for _ in range(500)}

        assert picks == {"A", "C"}

    def test_roulette_is_proportional_to_fitness(self):
        """Selection frequency follows P = f / sum(f)."""
        rng = random.Random(0)
        picks = Counter(
            roulette_selection(["A", "B"], [1, 3], rng) for _ in range(4000)
        )

        assert 0.7 < picks["B"] / 4000 < 0.8

    def test_roulette_all_zero_fitness_picks_randomly(self):
        """When every fitness is 0, roulette falls back to a uniform pick."""
        rng = random.Random(0)
        picks = {roulette_selection(["A", "B"], [0, 0], rng) for _ in range(100)}

        assert picks == {"A", "B"}

    def test_tournament_returns_best_of_contestants(self):
        """With k == population size the fittest always wins."""
        rng = random.Random(0)
        population = ["A", "B", "C", "D"]
        fitnesses = [3, 9, 1, 5]

        for _ in range(20):
            assert tournament_selection(population, fitnesses, rng, k=4) == "B"

    def test_tournament_accepts_negative_fitness(self):
        """Tournament does not depend on the fitness scale."""
        rng = random.Random(0)

        assert tournament_selection(["A", "B"], [-5, -1], rng, k=2) == "B"

    def test_tournament_larger_k_is_stronger(self):
        """A larger tournament picks the best individual more often."""
        rng = random.Random(0)
        population = list(range(10))
        fitnesses = list(range(10))

        def avg(k):
            picks = [
                tournament_selection(population, fitnesses, rng, k) for _ in range(2000)
            ]
            return sum(picks) / len(picks)

        assert avg(5) > avg(2)


class TestCrossover:
    """Tests for one-point and order crossover."""

    def test_one_point_notebook_example(self):
        """Notebook 8.7.6: cut after position 3 swaps the tails."""
        rng = random.Random(0)
        rng.randint = lambda a, b: 3  # force the cut point
        child1, child2 = one_point_crossover(
            [1, 0, 1, 1, 0, 0], [1, 1, 0, 1, 0, 1], rng
        )

        assert child1 == [1, 0, 1, 1, 0, 1]
        assert child2 == [1, 1, 0, 1, 0, 0]

    def test_one_point_does_not_modify_parents(self):
        """Parents are left untouched."""
        rng = random.Random(0)
        p1, p2 = [1, 1, 1, 1], [0, 0, 0, 0]
        one_point_crossover(p1, p2, rng)

        assert p1 == [1, 1, 1, 1]
        assert p2 == [0, 0, 0, 0]

    def test_one_point_children_use_parent_genes_in_place(self):
        """Every gene of a child comes from the parent at the same position."""
        rng = random.Random(1)
        for _ in range(50):
            p1 = [rng.randint(0, 1) for _ in range(8)]
            p2 = [rng.randint(0, 1) for _ in range(8)]
            c1, c2 = one_point_crossover(p1, p2, rng)
            for i in range(8):
                assert {c1[i], c2[i]} == {p1[i], p2[i]}

    def test_order_crossover_notebook_example(self):
        """Notebook 8.4.5: segment at positions 4..6 (1-based) is kept."""
        rng = random.Random(0)
        rng.sample = lambda population, k: [3, 5]  # force segment [3, 5] (0-based)
        child1, child2 = order_crossover(
            [1, 2, 3, 4, 5, 6, 7, 8], [3, 7, 5, 1, 6, 8, 2, 4], rng
        )

        assert child1 == [3, 7, 1, 4, 5, 6, 8, 2]
        assert child2 == [2, 3, 4, 1, 6, 8, 5, 7]

    def test_order_crossover_always_gives_valid_permutations(self):
        """The reason OX exists: children never repeat or miss a city."""
        rng = random.Random(0)
        for _ in range(500):
            p1 = rng.sample(range(10), 10)
            p2 = rng.sample(range(10), 10)
            for child in order_crossover(p1, p2, rng):
                assert sorted(child) == list(range(10))

    def test_one_point_on_permutations_can_be_invalid(self):
        """Plain cut-and-splice duplicates cities: [1,2,3,4] x [3,4,1,2]."""
        rng = random.Random(0)
        rng.randint = lambda a, b: 2
        child1, _ = one_point_crossover([1, 2, 3, 4], [3, 4, 1, 2], rng)

        assert child1 == [1, 2, 1, 2]
        assert sorted(child1) != [1, 2, 3, 4]

    def test_order_crossover_single_gene(self):
        """A permutation of size 1 is returned as is."""
        assert order_crossover([0], [0], random.Random(0)) == ([0], [0])


class TestMutation:
    """Tests for bit-flip, swap and inversion mutation."""

    def test_bit_flip_rate_zero_changes_nothing(self):
        assert bit_flip_mutation([1, 0, 1], 0.0, random.Random(0)) == [1, 0, 1]

    def test_bit_flip_rate_one_flips_everything(self):
        assert bit_flip_mutation([1, 0, 1], 1.0, random.Random(0)) == [0, 1, 0]

    def test_bit_flip_does_not_modify_input(self):
        chromosome = [1, 0, 1]
        bit_flip_mutation(chromosome, 1.0, random.Random(0))

        assert chromosome == [1, 0, 1]

    @pytest.mark.parametrize("mutation", [swap_mutation, inversion_mutation])
    def test_rate_zero_changes_nothing(self, mutation):
        assert mutation([0, 1, 2, 3], 0.0, random.Random(0)) == [0, 1, 2, 3]

    @pytest.mark.parametrize("mutation", [swap_mutation, inversion_mutation])
    def test_keeps_valid_permutation_and_input_untouched(self, mutation):
        rng = random.Random(0)
        original = list(range(10))
        for _ in range(200):
            mutated = mutation(original, 1.0, rng)
            assert sorted(mutated) == list(range(10))
        assert original == list(range(10))

    def test_swap_changes_exactly_two_positions(self):
        rng = random.Random(0)
        for _ in range(50):
            mutated = swap_mutation(list(range(10)), 1.0, rng)
            assert sum(a != b for a, b in zip(mutated, range(10))) == 2

    def test_inversion_notebook_example(self):
        """Notebook 8.4.6: reversing positions 2..5 (1-based)."""
        rng = random.Random(0)
        rng.sample = lambda population, k: [1, 4]  # 0-based positions
        mutated = inversion_mutation([1, 2, 3, 4, 5, 6], 1.0, rng)

        assert mutated == [1, 5, 4, 3, 2, 6]

    def test_permutation_mutation_on_single_gene(self):
        assert swap_mutation([0], 1.0, random.Random(0)) == [0]
        assert inversion_mutation([0], 1.0, random.Random(0)) == [0]
