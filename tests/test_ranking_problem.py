import pytest
from solver.ranking_problem import RankingProblem
from solver.positions import FIRST, LAST

def test_can_create_ranking_problem():
    RankingProblem()


def test_items_are_empty_on_creation():
    r = RankingProblem()
    assert(len(r._items) == 0)


def test_number_of_items_is_zero_on_creation():
    r = RankingProblem()
    assert(r._number_of_items == 0)


def test_first_variable_on_creation():
    r = RankingProblem()
    assert(r._variables[FIRST] == [0])


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

    assert(r._constraints[1][1] == ("Dog", "Cat"))
    assert(r._constraints[1][0]._func.__name__ == "not_equal")


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

    assert(r._constraints[1][1] == ("Dog", FIRST))
    assert(r._constraints[1][0]._func.__name__ == "not_equal")


def test_can_call_not_directly_above_or_below():
    r = RankingProblem()
    r.set_items(["Dog", "Cat"])
    r.not_directly_above_or_below("Dog", "Cat")


def test_not_directly_above_or_below_fails_on_unknown_item():
    r = RankingProblem()
    r.set_items(["Dog", "Cat"])
    with pytest.raises(ValueError, match="Kat not in Items"):
        r.not_directly_above_or_below("Dog", "Kat")




