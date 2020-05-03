statements = [
    "[Drink tea] not first",
    "[Boil water in the kettle] not last",
    "[Boil water in the kettle] before [Pour boiled water into cup]",
    "[Get a cup from the cupboard] before [Pour boiled water into cup]",
    "[Put tea bag into cup] after [Get a cup from the cupboard]",
    "[Put tea bag into cup] before [Drink tea]",
    "[Pour boiled water into cup] before [Drink tea]",
]

csv_export = """start,end,weight
Get_a_cup_from_the_cupboard,Put_tea_bag_into_cup,1
Get_a_cup_from_the_cupboard,Boil_water_in_the_kettle,2
Put_tea_bag_into_cup,Boil_water_in_the_kettle,1
Put_tea_bag_into_cup,Drink_tea,1
Put_tea_bag_into_cup,Pour_boiled_water_into_cup,1
Boil_water_in_the_kettle,Pour_boiled_water_into_cup,2
Boil_water_in_the_kettle,Put_tea_bag_into_cup,1
Pour_boiled_water_into_cup,Drink_tea,2
Pour_boiled_water_into_cup,Put_tea_bag_into_cup,1"""
