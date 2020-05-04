from typing import List
import networkx as nx
from .ranking_graph import RankingGraph
from .ranking_network import RankingNetwork


def calculate_demand(G):
    sc = list(nx.strongly_connected_components(G))
    sc_count = [len(x) for x in sc]
    sc_sum = sum(sc_count)
    sc_ratio = [(x / sc_sum) for x in sc_count]

    result = dict()

    for i, sc_entry in enumerate(sc):
        for sc_item in sc_entry:
            result[sc_item] = sc_ratio[i]
            G.nodes[sc_item]["capacity"] = sc_ratio[i]
    return result


def graph_stats(G):
    result = {}
    try:
        # https://networkx.github.io/documentation/stable/reference/algorithms/generated/networkx.algorithms.flow.min_cost_flow.html#networkx.algorithms.flow.min_cost_flow
        # demand maybe from strongly_connected_components
        # TODO: revisit this
        # calculate_demand(G)
        # result["min_cost_flow"] = nx.min_cost_flow(G, capacity="inverse_weight", weight="weight")

        result["pagerank"] = nx.pagerank(G)

        result["betweenness_centrality"] = nx.betweenness_centrality(G)

        result["degree_centrality"] = nx.degree_centrality(G)

        result["eccentricity"] = nx.eccentricity(G)

        result["average_node_connectivity"] = nx.average_node_connectivity(G)

        result["dominating_set"] = nx.dominating_set(G)

        result["strongly_connected_components"] = list(nx.strongly_connected_components(G))
    except Exception:
        pass

    return result


def stats_from_solutions(solutions: List[List[str]]):
    rg = RankingGraph(solutions)
    rn = RankingNetwork()
    rn = rn.build_from_ranking_graph(rg, True)
    return graph_stats(rn.G)


