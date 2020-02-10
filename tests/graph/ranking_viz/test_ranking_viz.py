from test_data import tea_steps
from test_data import roadmap_steps
from graph import generate_viz_from_statements


def test_ranking_viz_from_statements():
    expected = """strict digraph  {
Get_a_cup_from_the_cupboard [fillcolor="#ffffff", label="Get a cup from the cupboard", position=0, shape=rectangle, style=filled];
Put_tea_bag_into_cup [fillcolor="#cccccc", label="Put tea bag into cup", position=2, shape=rectangle, style=filled];
Boil_water_in_the_kettle [fillcolor="#e6e6e6", label="Boil water in the kettle", position=1, shape=rectangle, style=filled];
Pour_boiled_water_into_cup [fillcolor="#b3b3b3", label="Pour boiled water into cup", position=3, shape=rectangle, style=filled];
Drink_tea [fillcolor="#808080", label="Drink tea", position=5, shape=rectangle, style=filled];
Get_a_cup_from_the_cupboard -> Put_tea_bag_into_cup  [inverse_weight="1.0", penwidth=1];
Get_a_cup_from_the_cupboard -> Boil_water_in_the_kettle  [color=red, inverse_weight="0.5", penwidth=2];
Put_tea_bag_into_cup -> Boil_water_in_the_kettle  [inverse_weight="1.0", penwidth=1];
Put_tea_bag_into_cup -> Drink_tea  [color=red, inverse_weight="1.0", penwidth=1];
Put_tea_bag_into_cup -> Pour_boiled_water_into_cup  [inverse_weight="1.0", penwidth=1];
Boil_water_in_the_kettle -> Pour_boiled_water_into_cup  [color=red, inverse_weight="0.5", penwidth=2];
Boil_water_in_the_kettle -> Put_tea_bag_into_cup  [color=red, inverse_weight="1.0", penwidth=1];
Pour_boiled_water_into_cup -> Drink_tea  [color=red, inverse_weight="0.5", penwidth=2];
Pour_boiled_water_into_cup -> Put_tea_bag_into_cup  [inverse_weight="1.0", penwidth=1];
}
"""

    result = generate_viz_from_statements(tea_steps, None)
    assert(str(result) == expected)


def test_ranking_viz_from_statements_normalised_penwidths():
    expected = """strict digraph  {
Better_support_for_entity_recognition [fillcolor="#ffffff", label="Better support for entity recognition", position=0, shape=rectangle, style=filled];
Typo_Correction [fillcolor="#ededed", label="Typo Correction", position=1, shape=rectangle, style=filled];
Project_Management [fillcolor="#dbdbdb", label="Project Management", position=2, shape=rectangle, style=filled];
Session_Management [fillcolor="#b6b6b6", label="Session Management", position=4, shape=rectangle, style=filled];
Normalise_penwidth_on_graph [fillcolor="#b6b6b6", label="Normalise penwidth on graph", position=4, shape=rectangle, style=filled];
Generation_of_Graph_Image [fillcolor="#a4a4a4", label="Generation of Graph Image", position=5, shape=rectangle, style=filled];
Resolving_insufficient_specified_constraints [fillcolor="#808080", label="Resolving insufficient specified constraints", position=7, shape=rectangle, style=filled];
Better_support_for_entity_recognition -> Typo_Correction  [color=red, inverse_weight="0.5", penwidth=2];
Typo_Correction -> Project_Management  [color=red, inverse_weight="0.5", penwidth=2];
Project_Management -> Session_Management  [color=red, inverse_weight="1.0", penwidth=1];
Project_Management -> Normalise_penwidth_on_graph  [color=red, inverse_weight="1.0", penwidth=1];
Session_Management -> Normalise_penwidth_on_graph  [inverse_weight="1.0", penwidth=1];
Session_Management -> Generation_of_Graph_Image  [color=red, inverse_weight="1.0", penwidth=1];
Normalise_penwidth_on_graph -> Generation_of_Graph_Image  [color=red, inverse_weight="1.0", penwidth=1];
Normalise_penwidth_on_graph -> Session_Management  [inverse_weight="1.0", penwidth=1];
Generation_of_Graph_Image -> Resolving_insufficient_specified_constraints  [color=red, inverse_weight="0.5", penwidth=2];
}
"""

    result = generate_viz_from_statements(roadmap_steps, None, max_pen_width = 6)
    assert(str(result) == expected)
