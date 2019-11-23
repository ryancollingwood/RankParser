from solver.ranking_problem import RankingProblem


def test_ranking_problem_is_first_correct():
    rp = RankingProblem()
    expected_results = [
        ("a", "b", "c"),
        ("a", "c", "b"),
    ]
    rp.set_items(["b", "c", "a"])

    rp.is_first("a")

    actual_results = rp.solve()

    assert(actual_results == expected_results)


