from solver.ranking_problem import RankingProblem


def test_can_create_ranking_problem():
    RankingProblem()


def test_items_are_empty_on_creation():
    r = RankingProblem()
    assert(len(r._items) == 0)


def test_number_of_items_is_zero_on_creation():
    r = RankingProblem()
    assert(r._number_of_items == 0)

