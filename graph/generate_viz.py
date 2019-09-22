from typing import List
from .ranking_graph import RankingGraph
from .ranking_network import RankingNetwork
from solver import RankingParser


def generate_viz_from_statements(statements: List[str], output_dot_viz: str):
    rp = RankingParser()
    rp.build()

    for step in statements:
        rp.parse(step)

    solutions = rp.solve()

    return generate_viz_from_solutions(solutions, output_dot_viz)


def generate_viz_from_solutions(solutions: List[List[str]], output_dot_viz: str):
    rg = RankingGraph(solutions)
    rn = RankingNetwork(rg)

    return rn.ranking_network_to_dot_viz(output_dot_viz)
