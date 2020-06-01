from typing import List, Tuple
from itertools import chain
from statistics import stdev
#from constraint import Problem
#from constraint import AllDifferentConstraint
from ortools.sat.python import cp_model
from .ranking_solver import RankingSolver
from .positions import FIRST, LAST, NEARBY, POSITIONS
from .criteria import is_before, is_after, is_within_range, is_just_before, is_just_after
from .variable_cleansor import clean_variable, fuzzy_match_variable


class RankingProblem():

    def __init__(self):
        super().__init__()
        self._model = cp_model.CpModel()
        self._results = list()
        self._variables = dict()
        self._constraints = list()
        self._nearby = 3

    def add_variable(self, name, min_value = 0, max_value = None):
        self._variables[name] = (min_value, max_value)

    def remove_variable(self, name):
        if name in self._variables:
            del self._variables[name]

    def add_variables(self, names, min_value = 0, max_value = None):
        for name in names:
            self.add_variable(name, min_value, max_value)

    def variable_domain(self, variable_name):
        return self._variables[variable_name]

    def _reset_vars(self):
        number_of_added_item = len(self.added_items)
        if number_of_added_item < 10:
            self._nearby = 3
        else:
            nearby_value = round(stdev(range(number_of_added_item)))
            self._nearby = nearby_value

    def add_rank_constraint(self, comparison_func, *items):

        for item in items:
            self.check_item_present(item)

        cleaned_items = [self.match_variable(x) for x in items]

        variable_items = list()
        for ci in cleaned_items:
            if isinstance(ci, int):
                variable_items.append(ci)
            else:
                variable_items.append(f"variables['{ci}']")

        new_constraint = comparison_func.format(*variable_items)

        if new_constraint not in self._constraints:
            self._constraints.append(
                new_constraint
            )

    @property
    def added_items(self) -> Tuple:
        """
        The items that have been added, to the ranking problem
        :return:
        """
        return tuple([x for x in self._variables if x not in POSITIONS])

    def set_items(self, items: list):
        self.add_variables([clean_variable(x) for x in items])

        return self

    def match_variable(self, item: str):
        if isinstance(item, int):
            return item

        if item not in POSITIONS:
            return fuzzy_match_variable(item, tuple(self._variables.keys()))
        return item

    def add_item(self, item: str):
        new_item = self.match_variable(item)
        self.add_variable(new_item)

        return self

    def remove_item(self, item: str):
        item_to_remove = self.match_variable(item)
        self.remove_variable(item_to_remove)

        return self

    def check_item_present(self, item):

        if isinstance(item, int):
            return True

        check_item = self.match_variable(item)

        if check_item not in POSITIONS + list(self._variables.keys()):
            raise ValueError(f"{item} not in Items")
        return True

    def not_equal(self, a: str, b: str):
        self.add_rank_constraint(
            "{} != {}",
            a, b,
        )

        return self

    def is_equal(self, a: str, b: str):
        self.add_rank_constraint(
            "{} == {}",
            a, b,
        )

        return self

    def not_last(self, item: str):
        self.not_equal(item, LAST)

        return self

    def is_last(self, item: str):
        self.is_equal(item, LAST)

        return self

    def not_first(self, item: str):
        self.not_equal(item, FIRST)

        return self

    def is_first(self, item: str):
        self.is_equal(item, FIRST)

        return self

    def not_directly_before_or_after(self, a: str, b: str):
        self.add_rank_constraint(
            "{} != {} - 1",
            a, b
        )

        self.add_rank_constraint(
            "{} != {} + 1",
            a, b
        )

        return self

    def is_before(self, a: str, b: str):
        self.add_rank_constraint(
            "{} < {}",
            a, b
        )

        return self

    def is_after(self, a: str, b: str):
        self.add_rank_constraint(
            "{} > {}",
            a, b
        )

        return self

    def is_just_before(self, a: int, b: int):
        self.add_rank_constraint(
            "{} >= {} - {}",
            a, b, NEARBY
        )

        self.add_rank_constraint(
            "{} < {}",
            a, b
        )
        return self

    def is_just_after(self, a: int, b: int):
        self.add_rank_constraint(
            "{} <= {} + {}",
            a, b, NEARBY
        )

        self.add_rank_constraint(
            "{} > {}",
            a, b
        )

        return self

    def is_nearby(self, a: int, b: int):

        self.add_rank_constraint(
            "{} >= {} - {}",
            a, b, NEARBY
        )

        self.add_rank_constraint(
            "{} <= {} + {}",
            a, b, NEARBY
        )

        return self

    def remove_last_constraint(self):
        if len(self._constraints) > 0:
            del self._constraints[-1]

        return self

    def number_of_constraints(self):
        return len(self._constraints)

    def solve(self) -> List[Tuple[str]]:
        result = []

        self._reset_vars()
        self._model = cp_model.CpModel()
        number_of_added_item = len(self._variables)

        variables = dict()

        for k, v in self._variables.items():
            range_min = v[0] if v[0] else 0
            range_max = v[1] if v[1] else number_of_added_item - 1
            variables[k] = self._model.NewIntVar(range_min, range_max, k)

        variables[FIRST] = 0
        variables[LAST] = number_of_added_item - 1
        variables[NEARBY] = self._nearby

        for c in self._constraints:
            self._model.Add(eval(c))

        # exclude positions
        constraint_variables = [v for k, v in variables.items() if k not in POSITIONS]

        self._model.AddAllDifferent(constraint_variables)

        solver = cp_model.CpSolver()
        solution_callback = RankingSolver(constraint_variables)

        status = solver.Solve(self._model)
        if status in [cp_model.OPTIMAL, cp_model.FEASIBLE]:
            status = solver.SearchForAllSolutions(self._model, solution_callback)
        else:
            return list()

        result = solution_callback.results

        result.sort()
        return result

    def variable_constraints_count(self):
        result = self.item_links
        for item in result:
            result[item] = len(result[item])

        # return the result sorted by count
        return {k: v for k, v in sorted(result.items(), key=lambda sort_item: sort_item[1])}

    @property
    def specified_constraints(self):
        return [x for x in self._constraints]

    @property
    def item_links(self):
        result = dict()
        relevant_constraints = self.specified_constraints
        variables = self._model._CpModel__model.variables

        for index, item in enumerate(variables):
            if item.name in POSITIONS:
                continue
            item_constraints = [x.linear.vars for x in relevant_constraints if index in x.linear.vars]
            result_indexes = set([x for x in list(chain(*item_constraints)) if x != index])
            result[item.name] = sorted([variables[x].name for x in result_indexes])
        return {k: v for k, v in sorted(result.items(), key=lambda item: len(item[1]))}

    def least_most_common_variable(self):
        counts = self.variable_constraints_count()
        keys = list(counts.keys())
        values = list(counts.values())
        item_links = self.item_links

        min_index = 0
        max_index = len(keys) - 1

        min_key = None
        max_key = None

        while min_index < max_index:
            min_key = keys[min_index]
            min_key_links = item_links[min_key]
            max_key = keys[max_index]
            max_key_links = item_links[max_key]

            if len(max_key_links) == len(keys) - 1:
                max_index -= 1
                continue

            if len(min_key_links) == len(keys) - 1:
                break

            if min_key in max_key_links:
                min_index += 1
                continue

            break

        return min_key, max_key
