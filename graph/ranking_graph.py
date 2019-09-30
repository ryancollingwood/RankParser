from collections import defaultdict
from copy import copy


class RankingGraph(object):
    def __init__(self, input_matrix = None):

        self._weights = dict()
        self._edges = list()
        self._node_positions = defaultdict(int)
        self._start_end_nodes = list()

        if input_matrix is not None:
            self._build(input_matrix)

    def __getitem__(self, item=None):
        if item is None:
            return self

        return self._weights[item]

    def _build(self, input_matrix):
        
        for row in input_matrix:
            start_end_pair = (row[0], row[-1],)
            if start_end_pair not in self._start_end_nodes:
                self._start_end_nodes.append(start_end_pair)

            for column_index in range(len(row)-1):
                current_step = row[column_index]
                next_step = row[column_index + 1]
                self.add_nodes(current_step, next_step)
                self._node_positions[current_step] += column_index

            # we'll miss the last one otherwise
            self._node_positions[row[-1]] += len(row) - 1

    def edges(self):
        return self._edges

    def node_positions(self):
        result = copy(self._node_positions)
        max_value = float(max(result.values()))
        total_items = len(result)

        for key in result:
            value = result[key]
            result[key] = int((value / max_value) * total_items)

        return result

    def add_nodes(self, start, end):
        edge_tuple = (start, end,)

        if edge_tuple not in self._edges:
            self._edges.append(edge_tuple)

        if start not in self._weights:
            self._weights[start] = defaultdict(int)

        self._weights[start][end] += 1

    def start_nodes(self):
        return list(self._weights.keys())

    def start_end_nodes(self):
        return self._start_end_nodes

    def weights(self):
        return self._weights
