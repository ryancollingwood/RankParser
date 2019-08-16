from solver.ranking_problem import RankingProblem
from solver.positions import FIRST


def test_ranking_problem_solve_not_equal_correct():

    expected_results = [
        ("Blue", "Green", "Red",),
        ("Blue", "Red", "Green",),
        ("Red", "Blue", "Green",),
        ('Red', 'Green', 'Blue',),
    ]

    r = RankingProblem()
    r.set_items(["Red", "Green", "Blue"])
    # given there's a constraints that .items must be different
    # will evaluate against FIRST
    r.not_equal("Green", FIRST)

    actual_results = r.solve()

    assert(actual_results == expected_results)

