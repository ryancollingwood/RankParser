import networkx as nx


class RankingNetwork(object):
    def __init__(self, ranking_graph = None):
        self._G = nx.DiGraph()

        if ranking_graph is not None:
            self.build_from_ranking_graph(ranking_graph)

    def add_edge(self, start, end, weight = None):
        self._G.add_edge(start, end, weight = weight)

    def nodes_names(self):
        return [x[0] for x in self._G.nodes]

    def build_from_ranking_graph(self, ranking_graph):
        for step in ranking_graph.edges():
            start = step[0]
            end = step[1]
            weight = ranking_graph[start][end]
            self.add_edge(start, end, weight)

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

    def heaviest_complete_paths(self, start, end):
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

    def ranking_network_to_dot_viz(self):
        a_graph = nx.nx_pydot.to_pydot(self._G)
        file_name = "dot_output.txt"

        with open(file_name, "w") as f:
            f.write(str(a_graph))

        return a_graph

