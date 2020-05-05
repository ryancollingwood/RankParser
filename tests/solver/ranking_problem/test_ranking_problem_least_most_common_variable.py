import pytest
from solver.ranking_problem import RankingProblem


def test_ranking_problem_variable_constraints_count():
    expected_results = {
        "Blue": 3,
        "Green": 3,
        "Red": 1,
        "Yellow": 1,
    }

    r = RankingProblem()
    r.set_items(["Red", "Blue", "Green", "Yellow"])
    r.not_directly_before_or_after("Blue", "Green")

    result = r.variable_constraints_count()

    try:
        assert(result == expected_results)
    except AssertionError:
        pytest.fail("Failed to get expected variable_constraints_count from RankingProblem")


def test_ranking_problem_least_most_common_variable():
    expected_results = ("Red", "Green")

    r = RankingProblem()
    r.set_items(["Red", "Blue", "Green", "Yellow"])
    r.not_directly_before_or_after("Blue", "Green")

    result = r.least_most_common_variable()

    try:
        assert(result == expected_results)
    except AssertionError:
        pytest.fail("Failed to get expected variable_constraints_count from RankingProblem")


def test_ranking_problem_least_most_common_variable_equal_counts():
    expected_results = ("Blue", "Yellow")

    r = RankingProblem()
    r.set_items(["Red", "Blue", "Green", "Yellow"])
    r.not_directly_before_or_after("Blue", "Green")
    r.not_directly_before_or_after("Red", "Yellow")

    result = r.least_most_common_variable()

    try:
        assert(result == expected_results)
    except AssertionError:
        pytest.fail("Failed to get expected variable_constraints_count when counts are equal from RankingProblem")


def test_ranking_problem_least_most_common_variable_returns_min_max():
    expected_results = ("Yellow", "Green")

    r = RankingProblem()
    r.set_items(["Red", "Blue", "Green", "Yellow"])
    r.is_before("Blue", "Green")
    r.is_before("Red", "Green")

    result = r.least_most_common_variable()

    try:
        assert(result == expected_results)
    except AssertionError:
        pytest.fail("Failed to get min and max counts items in variable_constraints_count from RankingProblem")


def test_ranking_problem_least_most_common_variable_unlinked_pair():
    expected_results = ("Orange", "Green")

    r = RankingProblem()
    r.set_items(["Red", "Blue", "Green", "Yellow", "Orange"])
    r.is_before("Blue", "Green")
    r.is_before("Red", "Green")
    r.is_before("Yellow", "Green")
    r.is_before("Red", "Yellow")
    r.is_before("Orange", "Green")

    result = r.least_most_common_variable()

    try:
        assert(result == expected_results)
    except AssertionError:
        pytest.fail("Failed to get min and max counts items in variable_constraints_count from RankingProblem")
