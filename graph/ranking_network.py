import networkx as nx
from .ranking_graph import RankingGraph
from .ranking_viz import digraph_to_dot_viz


class RankingNetwork(object):
    def __init__(self):
        self._G = nx.DiGraph()
        self.weighted_paths = dict()

        self.start_nodes = list()
        self.end_nodes = list()
        self.most_likely_path = list()
        self.node_positions = list()

    def add_edge(self, start, end, weight = None):
        self._G.add_edge(start, end, weight = weight, inverse_weight = 1.0 / weight)

    def nodes_names(self):
        return [x[0] for x in self._G.nodes]

    def build_from_ranking_graph(
            self,
            ranking_graph: RankingGraph,
            recursively_build = True
    ):
        for step in ranking_graph.edges():
            start = step[0]
            end = step[1]
            weight = ranking_graph[start][end]
            self.add_edge(start, end, weight)

        nodes = self._G.nodes(data=True)
        self.node_positions = ranking_graph.node_positions()
        self.start_nodes = ranking_graph.most_likely_start_nodes()
        self.end_nodes = ranking_graph.most_likely_end_nodes()

        for node in nodes:
            node[1]["position"] = self.node_positions[node[0]]

        for pair in ranking_graph.start_end_nodes():
            weighted_path_results = self.complete_paths_by_weight(pair[0], pair[1])
            path_weight = weighted_path_results[0]
            weighted_paths = weighted_path_results[1]

            if path_weight not in self.weighted_paths:
                self.weighted_paths[path_weight] = list()

            for path in weighted_paths:
                if path not in self.weighted_paths[path_weight]:
                    self.weighted_paths[path_weight].append(path)

                    if path[0] in self.start_nodes and path[-1] in self.end_nodes:
                        if path not in self.most_likely_path:
                            self.most_likely_path.append(path)

        if recursively_build:
            new_rn = RankingNetwork()
            return new_rn.build_from_ranking_graph(RankingGraph(self.most_likely_path), False)

        return self

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
                result_indexes.append(i)

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
        # todo temp
        # highlight_paths = self.most_likely_path
        highlight_paths = self.most_likely_path

        """
        perhaps seomtihing in networkx can help us?
        """

        """
        highlight_paths = [
            x[0] in self.start_nodes and
            x[-1] in self.end_nodes for x in
            highlight_paths
        ]
        """

        # TODO: highlight_paths might contain multiple paths, but we might
        # only want to highlight the path that has the items in the order
        # they most often appear in
        """
        [['Sue', 'Peter', 'John', 'Paul', 'Ryan'], 
        ['Sue', 'Ryan', 'John', 'Paul', 'Peter']]
        Peter has the most evidence to appear last
        """
        return digraph_to_dot_viz(
            self._G,
            highlight_paths = highlight_paths,
            output_dot_viz = filename,
            max_pen_width = max_pen_width,
        )
