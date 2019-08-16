from solver.ranking_problem import RankingProblem


def test_ranking_problem_solve_not_first_in_pair_correct():
    expected_results = [
        ("Red", "Blue",),
    ]

    r = RankingProblem()
    r.set_items({"Blue", "Red"})
    r.not_first("Blue")

    actual_results = r.solve()

    assert(actual_results == expected_results)


def test_ranking_problem_solve_not_first_correct():
    r = RankingProblem()
    r.set_items({
        "Blue", "Red", "Green", "Yellow", "Blue", "Purple"
    })
    r.not_first("Blue")

    actual_results = r.solve()

    for actual_result in actual_results:
        assert(actual_result[0] != "Blue")

