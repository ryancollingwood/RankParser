import pytest
from solver.ranking_problem import RankingProblem
from solver.positions import FIRST, LAST, NEARBY


def test_can_set_items():
    input_items = ["Cat", "Dog", "Mouse"]
    expected_items = ("Cat", "Dog", "Mouse",)

    r = RankingProblem()
    r.set_items(input_items)

    assert(expected_items == r._items)


def test_items_are_a_copy():
    input_items = ["Cat", "Dog", "Mouse"]
    expected_items = ("Cat", "Dog", "Mouse",)

    r = RankingProblem()
    r.set_items(input_items)
    input_items.append("Monkey")

    assert(not tuple(input_items) == r._items)
    assert(expected_items == r._items)


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

    allowed_variable_keys = test_items + [FIRST, LAST, NEARBY]

    for key in r._variables:
        assert(key in allowed_variable_keys)


def test_ranking_problem_set_items_bracket_notation():

    test_items = [
        "[Boil water in the kettle]",
        "[Get a cup from the cupboard]",
        "[Pour boiled water into cup]",
        "[Put tea bag into cup]",
        "[Drink tea]"
        ]

    expected_keys = [
        "Boil_water_in_the_kettle",
        "Get_a_cup_from_the_cupboard",
        "Pour_boiled_water_into_cup",
        "Put_tea_bag_into_cup",
        "Drink_tea"
    ]

    r = RankingProblem()
    r.set_items(test_items)

    allowed_variable_keys = expected_keys + [FIRST, LAST, NEARBY]

    for key in r._variables:
        assert(key in allowed_variable_keys)
