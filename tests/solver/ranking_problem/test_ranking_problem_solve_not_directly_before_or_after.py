from solver.ranking_problem import RankingProblem


def test_can_call_ranking_problem_not_directly_before_or_after():
    r = RankingProblem()
    r.set_items(["Read", "Blue", "Green", "Yellow"])
    r.not_directly_before_or_after("Blue", "Green")


def test_ranking_problem_not_directly_before_or_after_correct():

    expected_results = [
        ("Blue", "Red", "Green", "Yellow",),
        ("Blue", "Red", "Yellow", "Green",),
        ("Blue", "Yellow", "Green", "Red",),
        ("Blue", "Yellow", "Red", "Green",),

        ("Green", "Red", "Blue", "Yellow"),
        ("Green", "Red", "Yellow", "Blue"),
        ("Green", "Yellow", "Blue", "Red"),
        ("Green", "Yellow", "Red", "Blue"),

        ("Red", "Blue", "Yellow", "Green",),
        ("Red", "Green", "Yellow", "Blue",),

        ("Yellow", "Blue", "Red", "Green",),
        ("Yellow", "Green", "Red", "Blue",),
    ]

    r = RankingProblem()
    r.set_items(["Red", "Blue", "Green", "Yellow"])
    r.not_directly_before_or_after("Blue", "Green")

    actual_results = r.solve()

    assert(actual_results == expected_results)
