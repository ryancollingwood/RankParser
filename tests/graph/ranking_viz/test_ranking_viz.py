from test_data import tea_steps
from test_data import roadmap_steps
from graph import generate_viz_from_statements


def test_ranking_viz_from_statements():
    expected = """strict digraph  {
Boil_water_in_the_kettle [fillcolor="#e6e6e6", label="Boil water in the kettle", position=1, shape=rectangle, style=filled];
Get_a_cup_from_the_cupboard [fillcolor="#ffffff", label="Get a cup from the cupboard", position=0, shape=rectangle, style=filled];
Pour_boiled_water_into_cup [fillcolor="#b3b3b3", label="Pour boiled water into cup", position=3, shape=rectangle, style=filled];
Put_tea_bag_into_cup [fillcolor="#cccccc", label="Put tea bag into cup", position=2, shape=rectangle, style=filled];
Drink_tea [fillcolor="#808080", label="Drink tea", position=5, shape=rectangle, style=filled];
Boil_water_in_the_kettle -> Get_a_cup_from_the_cupboard  [color=red, penwidth=2];
Boil_water_in_the_kettle -> Pour_boiled_water_into_cup  [penwidth=2];
Boil_water_in_the_kettle -> Put_tea_bag_into_cup  [penwidth=1];
Get_a_cup_from_the_cupboard -> Pour_boiled_water_into_cup  [penwidth=1];
Get_a_cup_from_the_cupboard -> Put_tea_bag_into_cup  [color=red, penwidth=2];
Get_a_cup_from_the_cupboard -> Boil_water_in_the_kettle  [penwidth=2];
Pour_boiled_water_into_cup -> Put_tea_bag_into_cup  [penwidth=2];
Pour_boiled_water_into_cup -> Drink_tea  [color=red, penwidth=3];
Put_tea_bag_into_cup -> Drink_tea  [penwidth=2];
Put_tea_bag_into_cup -> Pour_boiled_water_into_cup  [color=red, penwidth=2];
Put_tea_bag_into_cup -> Boil_water_in_the_kettle  [penwidth=1];
}
"""

    result = generate_viz_from_statements(tea_steps, None)
    assert(str(result) == expected)


def test_ranking_viz_from_statements_normalised_penwidths():
    expected = """strict digraph  {
Better_support_for_entity_recognition [fillcolor="#ffffff", label="Better support for entity recognition", position=0, shape=rectangle, style=filled];
Normalise_penwidth_on_graph [fillcolor="#dbdbdb", label="Normalise penwidth on graph", position=2, shape=rectangle, style=filled];
Typo_Correction [fillcolor="#ededed", label="Typo Correction", position=1, shape=rectangle, style=filled];
Project_Management [fillcolor="#c9c9c9", label="Project Management", position=3, shape=rectangle, style=filled];
Generation_of_Graph_Image [fillcolor="#a4a4a4", label="Generation of Graph Image", position=5, shape=rectangle, style=filled];
Resolving_insufficient_specified_constraints [fillcolor="#808080", label="Resolving insufficient specified constraints", position=7, shape=rectangle, style=filled];
Session_Management [fillcolor="#a4a4a4", label="Session Management", position=5, shape=rectangle, style=filled];
Better_support_for_entity_recognition -> Normalise_penwidth_on_graph  [penwidth=1];
Better_support_for_entity_recognition -> Typo_Correction  [color=red, penwidth=6];
Normalise_penwidth_on_graph -> Typo_Correction  [penwidth=1];
Normalise_penwidth_on_graph -> Project_Management  [penwidth=1];
Normalise_penwidth_on_graph -> Generation_of_Graph_Image  [penwidth=1];
Normalise_penwidth_on_graph -> Session_Management  [penwidth=1];
Normalise_penwidth_on_graph -> Better_support_for_entity_recognition  [color=red, penwidth=1];
Typo_Correction -> Project_Management  [color=red, penwidth=6];
Typo_Correction -> Normalise_penwidth_on_graph  [penwidth=1];
Project_Management -> Generation_of_Graph_Image  [color=red, penwidth=3];
Project_Management -> Session_Management  [penwidth=2];
Project_Management -> Normalise_penwidth_on_graph  [penwidth=1];
Generation_of_Graph_Image -> Resolving_insufficient_specified_constraints  [color=red, penwidth=5];
Generation_of_Graph_Image -> Session_Management  [penwidth=2];
Resolving_insufficient_specified_constraints -> Session_Management  [color=red, penwidth=2];
Session_Management -> Resolving_insufficient_specified_constraints  [penwidth=2];
Session_Management -> Generation_of_Graph_Image  [penwidth=2];
Session_Management -> Normalise_penwidth_on_graph  [penwidth=1];
}
"""

    result = generate_viz_from_statements(roadmap_steps, None, max_pen_width = 6)
    assert(str(result) == expected)
