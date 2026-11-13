import random


def one_point_crossover(
    parent1: list, parent2: list, rng: random.Random
) -> tuple[list, list]:
    """
    One-point crossover for bit strings / vectors.

        Parent 1:  1 0 1 | 1 0 0          Child 1:  1 0 1 | 1 0 1
        Parent 2:  1 1 0 | 1 0 1    ->     Child 2:  1 1 0 | 1 0 0

    Args:
        parent1: First parent
        parent2: Second parent (same length)
        rng: Random number generator

    Returns:
        Two children (new lists)
    """
    size = len(parent1)
    if size < 2:
        return parent1[:], parent2[:]

    # Cut after position `cut` (1 .. size - 1, so both parts are non-empty)
    cut = rng.randint(1, size - 1)
    return parent1[:cut] + parent2[cut:], parent2[:cut] + parent1[cut:]


def order_crossover(
    parent1: list, parent2: list, rng: random.Random
) -> tuple[list, list]:
    """
    Order crossover (OX) for permutations. Children are always valid permutations.

    Keep a segment of one parent, fill the remaining positions (left to right)
    with the missing genes in the order they appear in the other parent.

        Parent 1:  1 2 3 [4 5 6] 7 8
        Parent 2:  3 7 5  1 6 8  2 4

        Child 1:   _ _ _  4 5 6  _ _   copy segment of parent 1
                   3 7 1 4 5 6 8 2     fill with parent 2 order: 3 7 1 8 2
        Child 2:   2 3 4 1 6 8 5 7     same, with roles swapped

    Args:
        parent1: First parent (a permutation)
        parent2: Second parent (a permutation of the same genes)
        rng: Random number generator

    Returns:
        Two children (new lists)
    """
    size = len(parent1)
    if size < 2:
        return parent1[:], parent2[:]

    # Segment [start, end] (inclusive) is kept from the donor parent
    start, end = sorted(rng.sample(range(size), 2))
    return (
        _order_child(parent1, parent2, start, end),
        _order_child(parent2, parent1, start, end),
    )


def _order_child(donor: list, filler: list, start: int, end: int) -> list:
    """Child = donor[start..end] + genes missing from it, in `filler` order."""
    kept = set(donor[start : end + 1])
    missing = iter(gene for gene in filler if gene not in kept)
    return [donor[i] if start <= i <= end else next(missing) for i in range(len(donor))]
