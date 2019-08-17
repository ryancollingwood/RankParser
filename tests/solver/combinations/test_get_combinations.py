import pytest
from solver.combinations import get_all_combinations


def test_can_call_get_all_combinations():
    get_all_combinations(["Red", "Blue"])


def test_get_all_combinations_empty():
    empty_results = [()]

    assert(get_all_combinations([]) == empty_results)


def test_get_all_combinations_correct():
    expected_results = [
        ("Blue", "Red",),
        ("Red", "Blue",),
    ]

    actual_results = get_all_combinations(["Red", "Blue"])
    assert(actual_results == expected_results)


def test_get_all_combinations_correct_but_out_of_sequence():
    expected_results_out_of_sequence = [
        ("Red", "Blue",),
        ("Blue", "Red",),
    ]

    actual_results = get_all_combinations(["Red", "Blue"])
    assert(actual_results != expected_results_out_of_sequence)
    assert(actual_results[0] == expected_results_out_of_sequence[1])
    assert (actual_results[1] == expected_results_out_of_sequence[0])


def test_get_all_combinations_excluding_supplied_correct():
    expected_results = [
        ("Blue", "Red",),
    ]

    actual_results = get_all_combinations(["Red", "Blue"], False)
    assert(actual_results == expected_results)


def test_get_all_combinations_excluding_supplied_incorrect():
    unexpected_results = [
        ("Red", "Blue",),
    ]

    actual_results = get_all_combinations(["Red", "Blue"], False)

    for unexpected_item in unexpected_results:
        with pytest.raises(ValueError, match=r".*is not in list"):
            actual_results.index(unexpected_item)
