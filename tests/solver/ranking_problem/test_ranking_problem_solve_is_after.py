import pytest
from solver.ranking_problem import RankingProblem
from solver.combinations import get_all_combinations
from solver.exceptions import UnsolvableModelError


def test_solve_is_after_fully_specified_correct():
    expected_results = [("Dog", "Cat", "Mouse",)]

    r = RankingProblem()
    r.set_items(["Dog", "Cat", "Mouse"])
    r.is_after("Cat", "Dog")
    r.is_after("Mouse", "Cat")

    actual_result = r.solve()
    assert(actual_result == expected_results)


def test_solve_is_after_fully_specified_incorrect():
    unexpected_results = get_all_combinations(
        ["Dog", "Cat", "Mouse"],
        include_passed_values=False
    )

    r = RankingProblem()
    r.set_items(["Dog", "Cat", "Mouse"])
    r.is_after("Cat", "Dog")
    r.is_after("Mouse", "Cat")

    actual_results = r.solve()

    for actual_result in actual_results:
        for unexpected_result in unexpected_results:
            assert(unexpected_result != actual_result)


def test_solve_is_after_unsolvable():
    r = RankingProblem()
    r.set_items(["Dog", "Cat"])
    r.is_after("Cat", "Dog")
    r.is_after("Dog", "Cat")

    with pytest.raises(UnsolvableModelError):
        r.solve()


def test_solve_is_after_partially_specified():

    expected_results = [
        ("Dog", "Cat", "Mouse",),
        ("Dog", "Mouse", "Cat",),
        ("Mouse", "Dog", "Cat",),
    ]

    r = RankingProblem()
    r.set_items(["Dog", "Cat", "Mouse"])
    r.is_after("Cat", "Dog")
    actual_results = r.solve()

    assert(len(actual_results) == 3)
    assert(actual_results[0] == expected_results[0])
    assert(actual_results[1] == expected_results[1])
    assert (actual_results[2] == expected_results[2])
