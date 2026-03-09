from itertools import permutations
from typing import List, Tuple


def get_all_combinations(values: List, include_passed_values: bool = True) -> List[Tuple]:
    result = list(permutations(values))
    result.sort()

    if not include_passed_values:
        result.remove(tuple(values))

    return result
