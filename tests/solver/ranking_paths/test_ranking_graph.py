from solver import RankingGraph


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
