from solver.ranking_problem import RankingProblem
from solver.combinations import get_all_combinations
from typing import List


def test_can_call_solve():
    r = RankingProblem()
    r.set_items(["Dog", "Cat", "Mouse"])
    r.is_after("Cat", "Dog")
    r.solve()


def test_solve_returns_list():
    expected_results = get_all_combinations(["Dog", "Cat", "Mouse"])

    r = RankingProblem()
    r.set_items(["Dog", "Cat", "Mouse"])
    actual_results = r.solve()

    assert(actual_results == expected_results)


def test_solve_returns_sorted_list():
    r = RankingProblem()
    r.set_items(["Dog", "Cat", "Mouse"])
    r.is_after("Cat", "Dog")
    assert(isinstance(r.solve(), List))


def test_solve_add_item_after_specifying_constraint():
    expected_results = [
        ("Dog", "Cat", "Mouse"),
        ('Dog', 'Mouse', 'Cat'),
        ("Mouse", "Dog", "Cat"),
    ]

    r = RankingProblem()
    r.set_items(["Cat", "Dog"])
    r.is_after("Cat", "Dog")
    r.add_item("Mouse")

    actual_results = r.solve()

    assert(actual_results == expected_results)


def test_can_solve_when_similar_steps():
    """
    New Email before Send Email
    Attach Image after Create New Email
    Send Email after Attach Image
    """
    expected_results = [
        ("New_Email", "Attach_Image", "Send_Email"),
    ]

    r = RankingProblem()

    for step_descriptions in [
        "New Email", "Send Email",
        "Attach Image", "Create New Email"
    ]:
        r.add_item(step_descriptions)

    r.is_before("New_Email", "Send_Email").\
        is_after("Attach_Image", "New_Email"). \
        is_after("Send_Email", "Attach_Image")

    actual_results = r.solve()

    assert (actual_results == expected_results)

