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

r.set_items(["Jessie", "Evan", "John", "Sarah", "Matt"]).\
    not_first("Jessie").not_last("Evan").\
    not_first("John").not_last("John").\
    is_before("Sarah", "Evan").\
    not_directly_before_or_after("Matt", "John").\
    not_directly_before_or_after("John", "Evan")

solutions = r.solve()
print("Total number of ways: {}".format(len(solutions)))

for s in solutions:
    print(s)
