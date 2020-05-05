import pytest
from constraint import AllDifferentConstraint
from solver.ranking_problem import RankingProblem


def test_can_call_specified_constraints():
    rp = RankingProblem()
    try:
        rp.specified_constraints
    except NameError:
        pytest.fail("Couldn't call specified_constraints on Ranking Problem")
    except:
        pass


def test_specified_constraints_doesnt_return_all_different_constraint():
    rp = RankingProblem()
    specified_constraints = rp.specified_constraints
    rp.set_items(["Red", "Blue", "Green"])
    rp.is_before("Red", "Green")

    for item in specified_constraints:
        assert(not(isinstance(item[0], AllDifferentConstraint)))


def test_specified_constraints_returns_empty_when_no_constraints_specified():
    rp = RankingProblem()
    specified_constraints = rp.specified_constraints

    assert(len(specified_constraints) == 0)
