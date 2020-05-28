from solver.ranking_problem import RankingProblem
from solver.positions import LAST, FIRST


def test_can_call_ranking_problem_remove_item():
    rp = RankingProblem()
    rp.remove_item("test")


def test_ranking_problem_remove_item_correct():
    expected_values = ("blue", "red",)

    rp = RankingProblem()
    rp.set_items(["blue", "red", "zero"])
    rp.remove_item("zero")

    assert(rp._items == expected_values)


def test_ranking_problem_remove_item_incorrect():
    unexpected_values = ("gamma",)

    rp = RankingProblem()
    rp.remove_item("beta")

    assert(rp._items != unexpected_values)


def test_item_variables_after_remove_item():
    test_item_a = "a"
    test_item_b = "b"
    test_item_c = "c"

    r = RankingProblem()
    r.set_items([test_item_a, test_item_b, test_item_c])
    assert(r.variable_domain(test_item_a) == [0, 2])
    assert(r.variable_domain(test_item_b) == [0, 2])
    assert(r.variable_domain(test_item_c) == [0, 2])

    r.remove_item(test_item_a)
    assert(r.variable_domain(test_item_b) == [0, 1])
    assert(r.variable_domain(test_item_c) == [0, 1])

    r.remove_item(test_item_b)
    assert(r.variable_domain(test_item_c) == [0, 0])


def test_last_variable_after_set_items():
    test_item_a = "a"
    test_item_b = "b"
    test_item_c = "c"

    r = RankingProblem()
    r.set_items([test_item_a, test_item_b, test_item_c])
    assert(r._variables[LAST] == [2])
    assert (r._variables[FIRST] == [0])

    r.remove_item(test_item_a)
    assert(r._variables[LAST] == [1])
    assert (r._variables[FIRST] == [0])

    r.remove_item(test_item_b)
    assert(r._variables[LAST] == [0])
    assert(r._variables[FIRST] == [0])


def test_ranking_problem_remove_item_no_duplicates():
    rp = RankingProblem()
    rp.set_items(["alpha", "gamma"])
    rp.remove_item("alpha")
    rp.remove_item("gamma")
    rp.remove_item("alpha")

    assert(rp._items == tuple())


def test_ranking_problem_remove_item_after_set_list():
    expected_values = ("alpha", "beta", "gamma")

    rp = RankingProblem()
    rp.set_items(["alpha", "beta", "delta", "gamma"])
    rp.remove_item("delta")

    assert(rp._items == expected_values)


def test_ranking_problem_remove_item_with_bracket_notation():
    expected_values = ("alpha", "beta", "gamma")

    rp = RankingProblem()
    rp.set_items(["alpha", "beta", "gamma", "delta_force"])
    rp.remove_item("[delta force]")

    assert(rp._items == expected_values)
