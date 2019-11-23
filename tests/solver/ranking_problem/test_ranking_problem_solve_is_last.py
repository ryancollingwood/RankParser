from solver.ranking_problem import RankingProblem


def test_ranking_problem_is_last_correct():
    rp = RankingProblem()
    expected_results = [
        ("b", "c", "a"),
        ("c", "b", "a"),
    ]
    rp.set_items(["a", "c", "b"])

    rp.is_last("a")

    actual_results = rp.solve()

    assert(actual_results == expected_results)


