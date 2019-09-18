from collections import defaultdict


class RankingGraph(object):
    def __init__(self, input_matrix = None):

        self._data = dict()
        self._edges = list()

        if input_matrix is not None:
            self._build(input_matrix)

    def __getitem__(self, item=None):
        if item is None:
            return self

        return self._data[item]

    def _build(self, input_matrix):
        for row in input_matrix:
            for column_index in range(len(row)-1):
                self.add_nodes(row[column_index], row[column_index + 1])

    def edges(self):
        return self._edges

    def add_nodes(self, start, end):
        edge_tuple = (start, end,)

        if edge_tuple not in self._edges:
            self._edges.append(edge_tuple)

        if start not in self._data:
            self._data[start] = defaultdict(int)

        self._data[start][end] += 1

    def start_nodes(self):
        return list(self._data.keys())

