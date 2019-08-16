import pytest
from solver.ranking_problem import RankingProblem
from solver.positions import FIRST, LAST


def test_can_set_items():
    test_items = ["Cat", "Dog", "Mouse"]
    r = RankingProblem()
    r.set_items(test_items)

    assert(test_items == r._items)


def test_items_are_a_copy():
    test_items = ["Cat", "Dog", "Mouse"]
    r = RankingProblem()
    r.set_items(test_items)
    test_items.append("Monkey")

    assert(not test_items == r._items)


def test_number_of_items_correct():
    test_items = ["Cat", "Dog", "Mouse"]
    r = RankingProblem()
    r.set_items(test_items)

    assert(r._number_of_items == len(test_items))


def test_cannot_change_items():
    test_items = ["Cat", "Dog", "Mouse"]
    r = RankingProblem()
    r.set_items(test_items)

    with pytest.raises(ValueError, match="Items Already Set"):
        r.set_items(["Foo", "Bar"])


def test_last_varible_after_set_items():
    test_items = ["Cat", "Dog", "Mouse"]
    r = RankingProblem()
    r.set_items(test_items)
    assert(r._variables[LAST] == [2])


def test_item_variables_after_set_items():
    test_items = ["Cat", "Dog", "Mouse"]
    r = RankingProblem()
    r.set_items(test_items)

    assert(r._variables["Cat"] == [0, 1, 2])
    assert(r._variables["Dog"] == [0, 1, 2])
    assert (r._variables["Mouse"] == [0, 1, 2])


def test_item_variable_names_after_set_items():
    test_items = ["Cat", "Dog", "Mouse"]
    r = RankingProblem()
    r.set_items(test_items)

    allowed_variable_keys = test_items + [FIRST, LAST]

    for key in r._variables:
        assert(key in allowed_variable_keys)
