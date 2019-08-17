from solver.ranking_problem import RankingProblem
from solver.combinations import get_all_combinations


def test_solve_is_before_fully_specified_correct():
    expected_results = [("Mouse", "Cat", "Dog",)]

    r = RankingProblem()
    r.set_items(["Dog", "Cat", "Mouse"])
    r.is_before("Cat", "Dog")
    r.is_before("Mouse", "Cat")

    actual_result = r.solve()
    assert(actual_result == expected_results)


def test_solve_is_before_fully_specified_incorrect():
    unexpected_results = get_all_combinations(
        ["Mouse", "Cat", "Dog"],
        include_passed_values=False
    )

    r = RankingProblem()
    r.set_items(["Dog", "Cat", "Mouse"])
    r.is_before("Cat", "Dog")
    r.is_before("Mouse", "Cat")

    actual_results = r.solve()

    for actual_result in actual_results:
        for unexpected_result in unexpected_results:
            assert(unexpected_result != actual_result)


def test_solve_is_before_unsolvable():
    unsolvable_results = []

    r = RankingProblem()
    r.set_items(["Dog", "Cat"])
    r.is_before("Cat", "Dog")
    r.is_before("Dog", "Cat")

    actual_results = r.solve()
    assert(actual_results == unsolvable_results)


def test_solve_is_before_partially_specified():

    expected_results = [
        ("Cat", "Dog", "Mouse",),
        ("Cat", "Mouse", "Dog",),
        ("Mouse", "Cat", "Dog",),
    ]

    r = RankingProblem()
    r.set_items(["Dog", "Cat", "Mouse"])
    r.is_before("Cat", "Dog")
    actual_results = r.solve()

    assert(len(actual_results) == 3)
    assert(actual_results[0] == expected_results[0])
    assert(actual_results[1] == expected_results[1])
    assert (actual_results[2] == expected_results[2])
