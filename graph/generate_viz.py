from typing import List
from .ranking_graph import RankingGraph
from .ranking_network import RankingNetwork
from solver import RankingParser


def generate_viz_from_statements(
        statements: List[str],
        output_dot_viz: str = None,
        max_pen_width = 12,
        only_show_highlighted_paths: bool = False,
):
    rp = RankingParser()
    rp.build()

    for step in statements:
        rp.parse(step)

    solutions = rp.solve()

    return generate_viz_from_solutions(
        solutions,
        output_dot_viz,
        max_pen_width = max_pen_width,
        only_show_highlighted_paths = only_show_highlighted_paths,
    )


def generate_viz_from_solutions(
        solutions: List[List[str]],
        output_dot_viz: str,
        max_pen_width = 12,
        only_show_highlighted_paths: bool = False,
):
    rg = RankingGraph(solutions)
    rn = RankingNetwork()
    rn = rn.build_from_ranking_graph(rg, True)

    return rn.to_dot_viz(
        output_dot_viz,
        max_pen_width = max_pen_width,
        only_show_highlighted_paths = only_show_highlighted_paths,
    )

