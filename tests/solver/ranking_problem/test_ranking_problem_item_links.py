import pytest
from solver.ranking_problem import RankingProblem


def test_can_call_item_links():
    r = RankingProblem()
    try:
        r.item_links
    except NameError:
        pytest.fail("Couldn't call item_links on RankingProblem")
    else:
        pass


def test_item_links():
    expected_results = {
        "Blue": ["Green"],
        "Orange": ["Green"],
        "Red": ["Green", "Yellow"],
        "Yellow": ["Green", "Red"],
        "Green": ["Blue", "Orange", "Red", "Yellow"]
    }

    r = RankingProblem()
    r.set_items(["Red", "Blue", "Green", "Yellow", "Orange"])
    r.is_before("Blue", "Green")
    r.is_before("Red", "Green")
    r.is_before("Yellow", "Green")
    r.is_before("Red", "Yellow")
    r.is_before("Orange", "Green")

    result = r.item_links

    assert(expected_results == result)

