import pytest
from solver.ranking_problem import RankingProblem
from solver.positions import FIRST, LAST


def test_can_call_not_equal():
    r = RankingProblem()
    r.set_items(["Dog", "Cat"])
    r.not_equal("Dog", "Cat")


def test_not_equal_fails_unknown_item():
    r = RankingProblem()
    r.set_items(["Dog", "Cat"])

    with pytest.raises(ValueError, match="Kat not in Items"):
        r.not_equal("Dog", "Kat")

    with pytest.raises(ValueError, match="Hound not in Items"):
        r.not_equal("Hound", "Cat")


def test_not_equal_constraint_set():
    r = RankingProblem()
    r.set_items(["Dog", "Cat"])
    r.not_equal("Dog", "Cat")

    assert(r._constraints[0].items == ("Dog", "Cat"))
    assert(str(r._constraints[0]) == "Dog != Cat")


def test_can_call_not_last():
    r = RankingProblem()
    r.set_items(["Dog"])
    r.not_last("Dog")


def test_not_last_fails_unknown_item():
    r = RankingProblem()
    with pytest.raises(ValueError, match="Dog not in Items"):
        r.not_last("Dog")


def test_not_last_constraint_set():
    r = RankingProblem()
    r.set_items(["Dog"])
    r.not_last("Dog")

    assert(r._constraints[1][1] == ("Dog", LAST))
    assert(r._constraints[1][0]._func.__name__ == "not_equal")


def test_can_call_not_first():
    r = RankingProblem()
    r.set_items(["Dog"])
    r.not_first("Dog")


def test_not_last_fails_unknown_item():
    r = RankingProblem()
    with pytest.raises(ValueError, match="Dog not in Items"):
        r.not_first("Dog")


def test_not_last_constraint_set():
    r = RankingProblem()
    r.set_items(["Dog"])
    r.not_first("Dog")

    assert(r._constraints[0].items == ("Dog", "FIRST"))
    assert(str(r._constraints[0]) == "Dog != FIRST")


def test_can_call_not_directly_above_or_below():
    r = RankingProblem()
    r.set_items(["Dog", "Cat"])
    r.not_directly_before_or_after("Dog", "Cat")


def test_not_directly_above_or_below_fails_on_unknown_item():
    r = RankingProblem()
    r.set_items(["Dog", "Cat"])
    with pytest.raises(ValueError, match="Kat not in Items"):
        r.not_directly_before_or_after("Dog", "Kat")


def test_not_directly_above_or_below_constraint_set():
    r = RankingProblem()
    r.set_items(["Dog", "Cat"])
    r.not_directly_before_or_after("Dog", "Cat")

    assert(r._constraints[0].items == ("Dog", "Cat"))
    assert(str(r._constraints[0]) == 'Dog != Cat - 1')
    assert(str(r._constraints[1]) == 'Dog != Cat + 1')


def test_can_call_is_before():
    r = RankingProblem()
    r.set_items(["Dog", "Cat"])
    r.is_before("Cat", "Dog")


def test_is_before_fails_on_unknown_item():
    r = RankingProblem()
    r.set_items(["Dog"])
    with pytest.raises(ValueError, match="Cat not in Items"):
        r.is_before("Cat", "Dog")


def test_is_before_constraint_set():
    r = RankingProblem()
    r.set_items(["Dog", "Cat"])
    r.is_before("Dog", "Cat")

    assert(r._constraints[1][1] == ("Dog", "Cat"))
    assert(r._constraints[1][0]._func.__name__ == "is_before")


def test_can_call_is_after():
    r = RankingProblem()
    r.set_items(["Dog", "Cat"])
    r.is_after("Cat", "Dog")


def test_is_before_fails_on_unknown_item():
    r = RankingProblem()
    r.set_items(["Dog"])
    with pytest.raises(ValueError, match="Cat not in Items"):
        r.is_after("Cat", "Dog")


def test_is_before_constraint_set():
    r = RankingProblem()
    r.set_items(["Dog", "Cat"])
    r.is_after("Dog", "Cat")

    assert(r._constraints[0].items == ("Dog", "Cat"))
    assert(str(r._constraints[0]) == "Dog > Cat")
