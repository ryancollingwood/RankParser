import networkx as nx
from .ranking_graph import RankingGraph
from .ranking_viz import digraph_to_dot_viz


class RankingNetwork(object):
    def __init__(self, ranking_graph = None):
        self._G = nx.DiGraph()
        self.weighted_paths = dict()

        if ranking_graph is not None:
            self.build_from_ranking_graph(ranking_graph)

    def add_edge(self, start, end, weight = None):
        self._G.add_edge(start, end, weight = weight)

    def nodes_names(self):
        return [x[0] for x in self._G.nodes]

    def build_from_ranking_graph(self, ranking_graph: RankingGraph):
        for step in ranking_graph.edges():
            start = step[0]
            end = step[1]
            weight = ranking_graph[start][end]
            self.add_edge(start, end, weight)

        nodes = self._G.nodes(data=True)
        node_positions = ranking_graph.node_positions()
        for node in nodes:
            node[1]["position"] = node_positions[node[0]]

        for pair in ranking_graph.start_end_nodes():
            weighted_path_results = self.complete_paths_by_weight(pair[0], pair[1])
            path_weight = weighted_path_results[0]
            weighted_paths = weighted_path_results[1]

            if path_weight not in self.weighted_paths:
                self.weighted_paths[path_weight] = list()

            for path in weighted_paths:
                self.weighted_paths[path_weight].append(path)

    def simplest_complete_paths(self, start, end):
        G = self._G
        result = [
            x for x in list(
                nx.all_simple_paths(G, start, end)
            ) if len(x) == len(G.nodes)
        ]
        return result

    def _get_path_weight(self, path):
        result = 0
        for i in range(len(path)-1):
            result += self._G.get_edge_data(path[i], path[i+1], default = 0)["weight"]
        return result

    def complete_paths_by_weight(self, start, end):
        result_indexes = []

        max_weight, max_weight_index = -1, -1

        # must have every node
        all_simple_paths = self.simplest_complete_paths(start, end)

        for i, path in enumerate(all_simple_paths):
            path_weight = self._get_path_weight(path)
            if path_weight >= max_weight:
                if path_weight > max_weight:
                    result_indexes = []

                max_weight = path_weight
                result_indexes.append(max_weight_index)

        if len(result_indexes) == 0:
            return None

        result_paths = []
        for i in result_indexes:
            result_paths.append(all_simple_paths[i])

        return max_weight, result_paths

    def heaviest_path(self):
        heaviest_path_value = max(self.weighted_paths.keys())
        return self.weighted_paths[heaviest_path_value]

    def ranking_network_to_dot_viz(self, filename, max_pen_width = 12):
        heaviest_path_value = max(self.weighted_paths.keys())
        highlight_paths = self.weighted_paths[heaviest_path_value]

        return digraph_to_dot_viz(
            self._G,
            highlight_paths = highlight_paths,
            output_dot_viz = filename,
            max_pen_width = max_pen_width,
        )
