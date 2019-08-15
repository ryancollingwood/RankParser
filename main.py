from solver.ranking_problem import RankingProblem

developers = ["Jessie", "Evan", "John", "Sarah", "Matt"]

"""
Jessie is not the best developer
Evan is not the worst developer
John is not the best developer or the worst developer
Sarah is a better developer than Evan
Matt is not directly below or above John as a developer
John is not directly below or above Evan as a developer
"""

r = RankingProblem()

r.set_items(["Jessie", "Evan", "John", "Sarah", "Matt"])

r.not_first("Jessie")

r.not_last("Evan")

r.not_first("John")
r.not_last("John")

r.is_before("Sarah", "Evan")

r.not_directly_before_or_after("Matt", "John")

r.not_directly_before_or_after("John", "Evan")

# TODO: Move this to the class
solutions = r.getSolutions()
print("Total number of ways: {}".format(len(solutions)))

for s in solutions:
    output = [""] * (len(developers))
    for person, position in s.items():
        if person in developers:
            output[position] = person
    print(output)
