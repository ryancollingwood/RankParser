from solver.ranking_problem import RankingProblem
from solver.combinations import get_all_combinations
from typing import List


def test_can_call_solve():
    r = RankingProblem()
    r.set_items(["Dog", "Cat", "Mouse"])
    r.is_after("Cat", "Dog")
    r.solve()


def test_solve_returns_list():
    expected_results = get_all_combinations(["Dog", "Cat", "Mouse"])

    r = RankingProblem()
    r.set_items(["Dog", "Cat", "Mouse"])
    actual_results = r.solve()

    assert(actual_results == expected_results)


def test_solve_returns_sorted_list():
    r = RankingProblem()
    r.set_items(["Dog", "Cat", "Mouse"])
    r.is_after("Cat", "Dog")
    assert(isinstance(r.solve(), List))


def test_solve_add_item_after_specifying_constraint():
    expected_results = [
        ("Dog", "Cat", "Mouse"),
        ('Dog', 'Mouse', 'Cat'),
        ("Mouse", "Dog", "Cat"),
    ]

    r = RankingProblem()
    r.set_items(["Cat", "Dog"])
    r.is_after("Cat", "Dog")
    r.add_item("Mouse")

    actual_results = r.solve()

    assert(actual_results == expected_results)

