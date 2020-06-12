from ortools.sat.python import cp_model
from .positions import POSITIONS


class RankingSolver(cp_model.CpSolverSolutionCallback):
    """Print intermediate solutions."""

    def __init__(self, variables):
        cp_model.CpSolverSolutionCallback.__init__(self)
        variable_len = len(variables)

        self.__variables = variables
        self.__solution_count = 0
        self.__max_solution_count = variable_len ** 3
        self.complete_results = True
        self.results = list()

    def on_solution_callback(self):
        if len(self.__variables) == 0:
            self.halt_incomplete_search()
            return

        self.__solution_count += 1
        callback_result = dict()
        for v in self.__variables:
            v_name = v._IntVar__var.name
            if v_name in POSITIONS:
                continue
            callback_result[self.Value(v)] = v_name

        new_result = tuple([x[1] for x in sorted(callback_result.items())])

        if new_result in self.results:
            self.StopSearch()
            return
        else:
            self.results.append(new_result)

        if self.__solution_count >= self.__max_solution_count:
            self.halt_incomplete_search()
            return

    def halt_incomplete_search(self):
        self.complete_results = False
        self.StopSearch()

    def solution_count(self):
        return self.__solution_count
