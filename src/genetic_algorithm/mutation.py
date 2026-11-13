import random


def bit_flip_mutation(chromosome: list, rate: float, rng: random.Random) -> list:
    """
    Flip each bit independently with probability `rate`.

        1 1 0 1 0 0  ->  1 1 0 1 0 1   (bit 6 flipped)

    Args:
        chromosome: Bit string (list of 0/1)
        rate: Probability of flipping EACH bit
        rng: Random number generator

    Returns:
        Mutated copy (new list)
    """
    return [1 - gene if rng.random() < rate else gene for gene in chromosome]


def swap_mutation(permutation: list, rate: float, rng: random.Random) -> list:
    """
    With probability `rate`, swap two random positions of a permutation.

        1 2 3 4 5 6  ->  1 5 3 4 2 6   (positions 2 and 5)

    Args:
        permutation: A permutation
        rate: Probability of mutating the WHOLE permutation
        rng: Random number generator

    Returns:
        Mutated copy (new list, a valid permutation)
    """
    mutated = permutation[:]
    if len(mutated) >= 2 and rng.random() < rate:
        i, j = rng.sample(range(len(mutated)), 2)
        mutated[i], mutated[j] = mutated[j], mutated[i]
    return mutated


def inversion_mutation(permutation: list, rate: float, rng: random.Random) -> list:
    """
    With probability `rate`, reverse a random segment of a permutation.

        1 2 3 4 5 6  ->  1 5 4 3 2 6   (positions 2..5)

    For TSP this is a 2-opt move: it only changes two edges of the tour.

    Args:
        permutation: A permutation
        rate: Probability of mutating the WHOLE permutation
        rng: Random number generator

    Returns:
        Mutated copy (new list, a valid permutation)
    """
    mutated = permutation[:]
    if len(mutated) >= 2 and rng.random() < rate:
        i, j = sorted(rng.sample(range(len(mutated)), 2))
        mutated[i : j + 1] = reversed(mutated[i : j + 1])
    return mutated
