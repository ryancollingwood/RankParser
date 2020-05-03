from typing import List, Tuple
from .ranking_graph import RankingGraph
from .ranking_network import RankingNetwork


def export_csv(solutions: List[Tuple[str]], output_filename: str):
    rg = RankingGraph(solutions)
    rn = RankingNetwork()
    rn = rn.build_from_ranking_graph(rg, True)

    return rn.to_csv(
        output_filename,
    )

