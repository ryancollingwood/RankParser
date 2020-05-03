from graph import RankingGraph
from graph import RankingNetwork


def test_ranking_network_can_create():
    test = RankingNetwork()
    assert(isinstance(test, RankingNetwork))


def simple_graph():
    return RankingGraph([
        ["a", "b", "c"]
    ])


def test_ranking_network_build_from_simple_ranking_graph():
    rg = simple_graph()

    test = RankingNetwork()
    test.build_from_ranking_graph(rg)


def test_ranking_networks_nodes_from_simple_ranking_graph():
    rg = simple_graph()

    test = RankingNetwork()
    test.build_from_ranking_graph(rg)
    assert(test.nodes_names() == ["a", "b", "c"])


def test_ranking_network_simplest_path_from_simple_ranking_graph():
    rg = simple_graph()

    test = RankingNetwork()
    test.build_from_ranking_graph(rg)
    result = test.simplest_complete_paths("a", "c")

    assert(result == [["a", "b", "c"]])


def tea_graph():
    return RankingGraph(
        [
            [
                'Boil_water_in_the_kettle', 'Get_a_cup_from_the_cupboard', 'Pour_boiled_water_into_cup',
                'Put_tea_bag_into_cup', 'Drink_tea'
            ],
            [
                'Boil_water_in_the_kettle', 'Get_a_cup_from_the_cupboard', 'Put_tea_bag_into_cup',
                'Pour_boiled_water_into_cup', 'Drink_tea'
            ],
            [
                'Get_a_cup_from_the_cupboard', 'Boil_water_in_the_kettle', 'Pour_boiled_water_into_cup',
                'Put_tea_bag_into_cup', 'Drink_tea'
            ],
            [
                'Get_a_cup_from_the_cupboard', 'Boil_water_in_the_kettle', 'Put_tea_bag_into_cup',
                'Pour_boiled_water_into_cup', 'Drink_tea'
            ],
            [
                'Get_a_cup_from_the_cupboard', 'Put_tea_bag_into_cup', 'Boil_water_in_the_kettle',
                'Pour_boiled_water_into_cup', 'Drink_tea'
            ]
        ]
    )


def test_ranking_network_simplest_path_from_ranking_graph():
    rg = tea_graph()

    test = RankingNetwork(rg)
    test.build_from_ranking_graph(rg)
    result = test.simplest_complete_paths("Boil_water_in_the_kettle", "Drink_tea")
    expected_result = [
        ['Boil_water_in_the_kettle', 'Get_a_cup_from_the_cupboard',
         'Pour_boiled_water_into_cup', 'Put_tea_bag_into_cup', 'Drink_tea'],
        ['Boil_water_in_the_kettle', 'Get_a_cup_from_the_cupboard',
         'Put_tea_bag_into_cup', 'Pour_boiled_water_into_cup', 'Drink_tea']
    ]

    assert(result == expected_result)


def test_ranking_network_heaviest_path_from_ranking_graph():
    rg = tea_graph()

    rn = RankingNetwork(rg)

    expected_result = (
        9, [
            ['Boil_water_in_the_kettle', 'Get_a_cup_from_the_cupboard',
             'Put_tea_bag_into_cup', 'Pour_boiled_water_into_cup', 'Drink_tea']
        ],
    )

    result = rn.complete_paths_by_weight("Boil_water_in_the_kettle", "Drink_tea")

    assert(result == expected_result)

    # temp
    rn.to_dot_viz("dot_output.txt")
