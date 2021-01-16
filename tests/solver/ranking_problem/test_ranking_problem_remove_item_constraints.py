from solver.ranking_problem import RankingProblem


def test_can_call_ranking_problem_remove_item_constraints():
    rp = RankingProblem()
    try:
        rp.remove_item_constraints()
    except NameError as e:
        raise e
    except Exception:
        pass


def test_ranking_problem_remove_item_constraints_invalid_item_no_exception():
    rp = RankingProblem()
    rp.add_item("Blue")

    rp.remove_item_constraints("Green")


def test_ranking_problem_remove_item_constraints_correct():
    rp = RankingProblem()
    rp.add_item("Blue")
    rp.add_item("Green")
    rp.add_item("Red")

    rp.is_after("Green", "Red")
    rp.is_after("Blue", "Green")

    expected_item_links = {
        "Blue": ["Green"],
        "Green": ["Blue"],
        "Red": []
    }

    rp.remove_item_constraints("Red")

    actual_item_links = rp.item_links

    assert(expected_item_links == actual_item_links)


def test_ranking_problem_remove_item_constraints_correct_longer_items():
    rp = RankingProblem()
    rp.add_item("Blue Berries")
    rp.add_item("Green Apples")
    rp.add_item("Red Grapes")

    rp.is_after("Green Apples", "Red Grapes")
    rp.is_after("Blue Berries", "Green Apples")

    expected_item_links = {
        "Blue_Berries": ["Green_Apples"],
        "Green_Apples": ["Blue_Berries"],
        "Red_Grapes": []
    }

    rp.remove_item_constraints("Red Grapes")

    actual_item_links = rp.item_links

    assert(expected_item_links == actual_item_links)
