import pytest
from solver.ranking_problem import RankingProblem


def test_can_call_ranking_problem_check_item_present():
    r = RankingProblem()
    r.set_items(["Red"])
    r.check_item_present("Red")


def test_ranking_problem_check_item_present_correct():
    r = RankingProblem()
    r.set_items(["Red",  "Green"])

    assert(r.check_item_present("Red"))
    assert(r.check_item_present("Green"))


def test_ranking_problem_check_item_present_returns_bool():
    r = RankingProblem()
    r.set_items(["Red", "Green"])

    assert(isinstance(r.check_item_present("Red"), bool))
    assert(isinstance(r.check_item_present("Green"), bool))


def test_ranking_problem_check_item_present_exception_on_invalid():
    r = RankingProblem()
    r.set_items(["Red", "Green"])

    with pytest.raises(ValueError, match="Blue not in Items"):
        assert(r.check_item_present("Blue"))

