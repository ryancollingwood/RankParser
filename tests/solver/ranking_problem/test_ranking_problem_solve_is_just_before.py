from solver.ranking_problem import RankingProblem


def test_ranking_problem_is_just_before_correct():
    rp = RankingProblem()
    expected_results = [('a', 'b', 'c', 'd', 'e'), ('a', 'b', 'd', 'c', 'e'), ('a', 'b', 'd', 'e', 'c'),
                        ('a', 'b', 'e', 'd', 'c'), ('a', 'c', 'b', 'd', 'e'), ('a', 'c', 'd', 'b', 'e'),
                        ('a', 'c', 'd', 'e', 'b'), ('a', 'c', 'e', 'd', 'b'), ('a', 'd', 'b', 'c', 'e'),
                        ('a', 'd', 'b', 'e', 'c'), ('a', 'd', 'c', 'b', 'e'), ('a', 'd', 'c', 'e', 'b'),
                        ('a', 'd', 'e', 'b', 'c'), ('a', 'd', 'e', 'c', 'b'), ('a', 'e', 'b', 'd', 'c'),
                        ('a', 'e', 'c', 'd', 'b'), ('a', 'e', 'd', 'b', 'c'), ('a', 'e', 'd', 'c', 'b'),
                        ('b', 'a', 'c', 'd', 'e'), ('b', 'a', 'c', 'e', 'd'), ('b', 'a', 'd', 'c', 'e'),
                        ('b', 'a', 'd', 'e', 'c'), ('b', 'a', 'e', 'c', 'd'), ('b', 'a', 'e', 'd', 'c'),
                        ('b', 'c', 'a', 'd', 'e'), ('b', 'c', 'a', 'e', 'd'), ('b', 'c', 'e', 'a', 'd'),
                        ('b', 'e', 'a', 'c', 'd'), ('b', 'e', 'a', 'd', 'c'), ('b', 'e', 'c', 'a', 'd'),
                        ('c', 'a', 'b', 'd', 'e'), ('c', 'a', 'b', 'e', 'd'), ('c', 'a', 'd', 'b', 'e'),
                        ('c', 'a', 'd', 'e', 'b'), ('c', 'a', 'e', 'b', 'd'), ('c', 'a', 'e', 'd', 'b'),
                        ('c', 'b', 'a', 'd', 'e'), ('c', 'b', 'a', 'e', 'd'), ('c', 'b', 'e', 'a', 'd'),
                        ('c', 'e', 'a', 'b', 'd'), ('c', 'e', 'a', 'd', 'b'), ('c', 'e', 'b', 'a', 'd'),
                        ('e', 'a', 'b', 'c', 'd'), ('e', 'a', 'b', 'd', 'c'), ('e', 'a', 'c', 'b', 'd'),
                        ('e', 'a', 'c', 'd', 'b'), ('e', 'a', 'd', 'b', 'c'), ('e', 'a', 'd', 'c', 'b'),
                        ('e', 'b', 'a', 'c', 'd'), ('e', 'b', 'a', 'd', 'c'), ('e', 'b', 'c', 'a', 'd'),
                        ('e', 'c', 'a', 'b', 'd'), ('e', 'c', 'a', 'd', 'b'), ('e', 'c', 'b', 'a', 'd')]

    rp.set_items(["a", "b", "c", "d", "e"])

    rp.is_just_before("a", "d")

    actual_results = rp.solve()

    assert (actual_results == expected_results)
