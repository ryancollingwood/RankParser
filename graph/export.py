from typing import List, Tuple
from .ranking_graph import RankingGraph
from .ranking_network import RankingNetwork
from input_output import check_file_extension


def export_csv(solutions: List[Tuple[str]], output_filename: str):
    rg = RankingGraph(solutions)
    rn = RankingNetwork()
    rn = rn.build_from_ranking_graph(rg, True)

    return rn.to_csv(
        check_file_extension(output_filename, "csv"),
    )


def export_highlighted_path(solutions):
    rg = RankingGraph(solutions)
    rn = RankingNetwork()
    rn = rn.build_from_ranking_graph(rg, True)

    return rn.distill_highlight_path()
