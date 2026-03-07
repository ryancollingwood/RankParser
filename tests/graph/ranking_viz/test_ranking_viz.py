from test_data import tea_steps
from test_data import roadmap_steps

from graph import generate_viz_from_statements


def test_ranking_viz_from_statements():
    expected = """strict digraph {
Get_a_cup_from_the_cupboard [position=0, shape=rectangle, style=filled, label="Get a cup from the cupboard", fillcolor="#ffffff"];
Put_tea_bag_into_cup [position=2, shape=rectangle, style=filled, label="Put tea bag into cup", fillcolor="#cccccc"];
Boil_water_in_the_kettle [position=1, shape=rectangle, style=filled, label="Boil water in the kettle", fillcolor="#e6e6e6"];
Pour_boiled_water_into_cup [position=3, shape=rectangle, style=filled, label="Pour boiled water into cup", fillcolor="#b3b3b3"];
Drink_tea [position=5, shape=rectangle, style=filled, label="Drink tea", fillcolor="#808080"];
Get_a_cup_from_the_cupboard -> Put_tea_bag_into_cup [inverse_weight=1.0, penwidth=1];
Get_a_cup_from_the_cupboard -> Boil_water_in_the_kettle [inverse_weight=0.5, penwidth=2, color=red];
Put_tea_bag_into_cup -> Boil_water_in_the_kettle [inverse_weight=1.0, penwidth=1];
Put_tea_bag_into_cup -> Drink_tea [inverse_weight=1.0, penwidth=1, color=red];
Put_tea_bag_into_cup -> Pour_boiled_water_into_cup [inverse_weight=1.0, penwidth=1];
Boil_water_in_the_kettle -> Pour_boiled_water_into_cup [inverse_weight=0.5, penwidth=2, color=red];
Boil_water_in_the_kettle -> Put_tea_bag_into_cup [inverse_weight=1.0, penwidth=1, color=red];
Pour_boiled_water_into_cup -> Drink_tea [inverse_weight=0.5, penwidth=2, color=red];
Pour_boiled_water_into_cup -> Put_tea_bag_into_cup [inverse_weight=1.0, penwidth=1];
}
"""

    result = generate_viz_from_statements(tea_steps, None)
    assert(str(result) == expected)


def test_ranking_viz_from_statements_normalised_penwidths():
    expected = """strict digraph {
Better_support_for_entity_recognition [position=0, shape=rectangle, style=filled, label="Better support for entity recognition", fillcolor="#ffffff"];
Typo_Correction [position=1, shape=rectangle, style=filled, label="Typo Correction", fillcolor="#ededed"];
Project_Management [position=2, shape=rectangle, style=filled, label="Project Management", fillcolor="#dbdbdb"];
Session_Management [position=4, shape=rectangle, style=filled, label="Session Management", fillcolor="#b6b6b6"];
Normalise_penwidth_on_graph [position=4, shape=rectangle, style=filled, label="Normalise penwidth on graph", fillcolor="#b6b6b6"];
Generation_of_Graph_Image [position=5, shape=rectangle, style=filled, label="Generation of Graph Image", fillcolor="#a4a4a4"];
Resolving_insufficient_specified_constraints [position=7, shape=rectangle, style=filled, label="Resolving insufficient specified constraints", fillcolor="#808080"];
Better_support_for_entity_recognition -> Typo_Correction [inverse_weight=0.5, penwidth=2, color=red];
Typo_Correction -> Project_Management [inverse_weight=0.5, penwidth=2, color=red];
Project_Management -> Session_Management [inverse_weight=1.0, penwidth=1, color=red];
Project_Management -> Normalise_penwidth_on_graph [inverse_weight=1.0, penwidth=1, color=red];
Session_Management -> Normalise_penwidth_on_graph [inverse_weight=1.0, penwidth=1];
Session_Management -> Generation_of_Graph_Image [inverse_weight=1.0, penwidth=1, color=red];
Normalise_penwidth_on_graph -> Generation_of_Graph_Image [inverse_weight=1.0, penwidth=1, color=red];
Normalise_penwidth_on_graph -> Session_Management [inverse_weight=1.0, penwidth=1];
Generation_of_Graph_Image -> Resolving_insufficient_specified_constraints [inverse_weight=0.5, penwidth=2, color=red];
}
"""

    result = generate_viz_from_statements(roadmap_steps, None, max_pen_width = 6)
    assert(str(result) == expected)
