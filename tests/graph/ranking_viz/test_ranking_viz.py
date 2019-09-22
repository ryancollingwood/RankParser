from test_data import tea_steps
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

