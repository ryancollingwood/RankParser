from solver.ranking_problem import RankingProblem


def test_can_call_ranking_problem_remove_last_constraint():
    rank_prob = RankingProblem()
    rank_prob.remove_last_constraint()


def test_ranking_problem_remove_last_constraint_returns_self():
    rank_prob = RankingProblem()
    rank_prob_id = id(rank_prob)
    compare_id = id(rank_prob.remove_last_constraint())
    assert(rank_prob_id == compare_id)


def test_ranking_problem_remove_last_constraint_removes_constraint():
    rank_prob = RankingProblem()
    rank_prob.set_items(["Huey", "Dewey", "Louie"]).\
        is_before("Louie", "Dewey")

    number_of_constraints = rank_prob.number_of_constraints()
    rank_prob.remove_last_constraint()

    assert(number_of_constraints == rank_prob.number_of_constraints() + 1)

