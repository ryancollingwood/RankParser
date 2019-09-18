from solver import RankingProblem
from solver import RankingGraph

def test_paths():
    ranking_problem = RankingProblem()

    ranking_problem.set_items([
        "Boil water in the kettle",
        "Pour boiled water into cup",
        "Get a cup from the cupboard",
        "Put tea bag into cup",
        "Drink tea",
    ])

    ranking_problem.not_first("Drink tea").\
        not_last("Boil water in the kettle").\
        is_before("Boil water in the kettle", "Pour boiled water into cup").\
        is_before("Get a cup from the cupboard", "Pour boiled water into cup").\
        is_after("Put tea bag into cup", "Get a cup from the cupboard").\
        is_before("Put tea bag into cup", "Drink tea").\
        is_before("Pour boiled water into cup", "Drink tea")

    solutions = ranking_problem.solve()


def test_ranking_graph_can_create():
    test = RankingGraph()
    assert(isinstance(test, RankingGraph))


def test_ranking_graph_add_item():
    test = RankingGraph()
    test.add_nodes("a", "b")

    assert(test["a"]["b"] == 1)


def test_ranking_graph_add_item_stays_in_order():

    test = RankingGraph()
    test.add_nodes("z", "b")
    test.add_nodes("z", "a")
    test.add_nodes("a", "b")
    test.add_nodes("b", "a")

    assert(test.edges() == [
        ("z", "b",),
        ("z", "a",),
        ("a", "b",),
        ("b", "a",),
    ])


def test_ranking_graph_add_item_no_duplicates():

    test = RankingGraph()
    test.add_nodes("z", "b")
    test.add_nodes("z", "b")
    test.add_nodes("z", "b")

    assert(test.edges() == [("z", "b",)])


def test_ranking_graph_add_item_weights():
    test = RankingGraph()
    test.add_nodes("z", "b")
    test.add_nodes("z", "a")
    test.add_nodes("z", "b")

    assert(test["z"]["b"] == 2)
    assert (test["z"]["a"] == 1)


def test_ranking_graph_build_from_matrix():
    data = [
        ["a", "b", "c", "d"],
        ["z", "a", "c", "b"]
    ]

    test = RankingGraph(data)

    expected_edges = [
        ("a", "b",),
        ("b", "c"),
        ("c", "d"),
        ("z", "a"),
        ("a", "c"),
        ("c", "b"),
    ]

    assert(test.edges() == expected_edges)
