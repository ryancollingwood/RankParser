from fuzzywuzzy import process
from copy import copy
from typing import Tuple


def clean_variable(item: str):
    new_item = copy(item)
    return new_item.replace("[", "").replace("]", "").strip().replace(" ", "_")


def match_variable(
        item: str,
        existing_items: Tuple,
        tolerance: int = 90
):
    if len(existing_items) == 0:
        return clean_variable(item)

    # replacing _ with spaces so that fuzzy wuzzy can tokenize
    best_match = process.extractOne(
        item,
        [x.replace("_", " ") for x in existing_items],
    )

    result = item
    if best_match[1] >= tolerance:
        result = best_match[0]

    return clean_variable(result)


