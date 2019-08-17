from itertools import permutations
from typing import List


def get_all_combinations(values: List, include_passed_values = True):
    result = list(permutations(values))
    result.sort()

    if not include_passed_values:
        result.remove(tuple(values))

    return result
