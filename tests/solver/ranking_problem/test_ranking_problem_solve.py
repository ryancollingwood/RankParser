from solver.ranking_problem import RankingProblem
from solver.combinations import get_all_combintations
from typing import List


def test_can_call_solve():
    r = RankingProblem()
    r.set_items(["Dog", "Cat", "Mouse"])
    r.is_after("Cat", "Dog")
    r.solve()


def test_solve_returns_list():
    expected_results = get_all_combintations(["Dog", "Cat", "Mouse"])

    r = RankingProblem()
    r.set_items(["Dog", "Cat", "Mouse"])
    actual_results = r.solve()

    assert(actual_results == expected_results)


def test_solve_returns_sorted_list():
    r = RankingProblem()
    r.set_items(["Dog", "Cat", "Mouse"])
    r.is_after("Cat", "Dog")
    assert(isinstance(r.solve(), List))

