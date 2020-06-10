from solver.ranking_problem import RankingProblem
from solver.positions import LAST, FIRST


def test_can_call_ranking_problem_add_item():
    rp = RankingProblem()
    rp.add_item("test")


def test_ranking_problem_add_item_correct():
    expected_values = ("test",)

    rp = RankingProblem()
    rp.add_item("test")

    assert(rp._items == expected_values)


def test_ranking_problem_add_item_incorrect():
    unexpected_values = ("gamma",)

    rp = RankingProblem()
    rp.add_item("beta")

    assert(rp._items != unexpected_values)


def test_item_variables_after_add_item():
    test_item_a = "a"
    test_item_b = "b"
    test_item_c = "c"

    r = RankingProblem()

    r.add_item(test_item_a)
    assert(r.variable_domain(test_item_a) == (0, None))

    r.add_item(test_item_b)
    assert(r.variable_domain(test_item_a) == (0, None))
    assert(r.variable_domain(test_item_b) == (0, None))

    r.add_item(test_item_c)
    assert(r.variable_domain(test_item_a) == (0, None))
    assert(r.variable_domain(test_item_b) == (0, None))
    assert(r.variable_domain(test_item_c) == (0, None))


def test_ranking_problem_add_item_no_duplicates():
    expected_items = ("alpha", "gamma",)

    rp = RankingProblem()
    rp.add_item("alpha")
    rp.add_item("gamma")
    rp.add_item("alpha")

    assert(rp._items == expected_items)


def test_ranking_problem_add_item_after_set_list():
    expected_values = ("alpha", "beta", "gamma", "delta")

    rp = RankingProblem()
    rp.set_items(["alpha", "beta", "gamma"])
    rp.add_item("delta")

    assert(rp._items == expected_values)


def test_ranking_problem_add_item_with_bracket_notation():
    expected_values = ("alpha", "beta", "gamma", "delta_force")

    rp = RankingProblem()
    rp.set_items(["alpha", "beta", "gamma"])
    rp.add_item("[delta force]")

    assert(rp._items == expected_values)
