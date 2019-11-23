from solver.ranking_problem import RankingProblem


def test_ranking_problem_is_just_after_correct():
    rp = RankingProblem()
    expected_results = [('b', 'c', 'd', 'a', 'e'), ('b', 'c', 'd', 'e', 'a'), ('b', 'c', 'e', 'd', 'a'),
                        ('b', 'd', 'a', 'c', 'e'), ('b', 'd', 'a', 'e', 'c'), ('b', 'd', 'c', 'a', 'e'),
                        ('b', 'd', 'c', 'e', 'a'), ('b', 'd', 'e', 'a', 'c'), ('b', 'd', 'e', 'c', 'a'),
                        ('b', 'e', 'c', 'd', 'a'), ('b', 'e', 'd', 'a', 'c'), ('b', 'e', 'd', 'c', 'a'),
                        ('c', 'b', 'd', 'a', 'e'), ('c', 'b', 'd', 'e', 'a'), ('c', 'b', 'e', 'd', 'a'),
                        ('c', 'd', 'a', 'b', 'e'), ('c', 'd', 'a', 'e', 'b'), ('c', 'd', 'b', 'a', 'e'),
                        ('c', 'd', 'b', 'e', 'a'), ('c', 'd', 'e', 'a', 'b'), ('c', 'd', 'e', 'b', 'a'),
                        ('c', 'e', 'b', 'd', 'a'), ('c', 'e', 'd', 'a', 'b'), ('c', 'e', 'd', 'b', 'a'),
                        ('d', 'a', 'b', 'c', 'e'), ('d', 'a', 'b', 'e', 'c'), ('d', 'a', 'c', 'b', 'e'),
                        ('d', 'a', 'c', 'e', 'b'), ('d', 'a', 'e', 'b', 'c'), ('d', 'a', 'e', 'c', 'b'),
                        ('d', 'b', 'a', 'c', 'e'), ('d', 'b', 'a', 'e', 'c'), ('d', 'b', 'c', 'a', 'e'),
                        ('d', 'b', 'e', 'a', 'c'), ('d', 'c', 'a', 'b', 'e'), ('d', 'c', 'a', 'e', 'b'),
                        ('d', 'c', 'b', 'a', 'e'), ('d', 'c', 'e', 'a', 'b'), ('d', 'e', 'a', 'b', 'c'),
                        ('d', 'e', 'a', 'c', 'b'), ('d', 'e', 'b', 'a', 'c'), ('d', 'e', 'c', 'a', 'b'),
                        ('e', 'b', 'c', 'd', 'a'), ('e', 'b', 'd', 'a', 'c'), ('e', 'b', 'd', 'c', 'a'),
                        ('e', 'c', 'b', 'd', 'a'), ('e', 'c', 'd', 'a', 'b'), ('e', 'c', 'd', 'b', 'a'),
                        ('e', 'd', 'a', 'b', 'c'), ('e', 'd', 'a', 'c', 'b'), ('e', 'd', 'b', 'a', 'c'),
                        ('e', 'd', 'b', 'c', 'a'), ('e', 'd', 'c', 'a', 'b'), ('e', 'd', 'c', 'b', 'a')]

    rp.set_items(["a", "b", "c", "d", "e"])

    rp.is_just_after("a", "d")

    actual_results = rp.solve()

    assert (actual_results == expected_results)
