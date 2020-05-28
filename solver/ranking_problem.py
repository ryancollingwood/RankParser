from typing import List, Tuple
from itertools import chain
from statistics import stdev
#from constraint import Problem
#from constraint import AllDifferentConstraint
from ortools.sat.python import cp_model
from .ranking_solver import RankingSolver
from .positions import FIRST, LAST, NEARBY, POSITIONS
from .criteria import is_equal, not_equal
from .criteria import not_directly_before, not_directly_after
from .criteria import is_before, is_after
from .criteria import is_within_range, is_just_before, is_just_after
from .variable_cleansor import clean_variable, fuzzy_match_variable


class RankingProblem():

    def __init__(self):
        super().__init__()
        self._model = cp_model.CpModel()
        self._results = list()
        self._items = tuple()
        self._number_of_items = 0
        self._variables = dict()
        self._constraints = list()

    def addVariable(self, name, min_value = 0, max_value = None):
        if max_value is None:
            range_max_value = len(self.added_items) - 1
        else:
            range_max_value = max_value

        if name not in self._variables:
            self._variables[str(name)] = self._model.NewIntVar(min_value, range_max_value, str(name))
        else:
            # self._variables[str(name)]._IntVar__var.domain.extend([min_value, max_value])
            self._variables[str(name)]._IntVar__var.domain.pop()
            self._variables[str(name)]._IntVar__var.domain.pop()
            self._variables[str(name)]._IntVar__var.domain.extend([min_value, max_value])

    def addVariables(self, names, min_value = 0, max_value = None):
        for name in names:
            self.addVariable(name, min_value, max_value)

    def variable_domain(self, variable_name):
        return self._variables[variable_name]._IntVar__var.domain

    def _reset_vars(self):
        self._number_of_items = len(self.added_items)

        self.addVariable(FIRST, 0, 0)

        self.addVariable(LAST, self._number_of_items, self._number_of_items)

        if self._number_of_items < 10:
            self.addVariable(NEARBY, 1, 3)
        else:
            nearby_value = round(stdev(range(self._number_of_items)))
            self.addVariable(NEARBY, 1, nearby_value)

        self.addVariables(self._items, 0, self._number_of_items - 1)

        self._model.AddAllDifferent([self._variables[x] for x in self.added_items])

    def add_rank_constraint(self, comparison_func, *items):
        cleaned_items = [self.match_variable(x) for x in items]

        variables = [x for x in [self._variables[y] for y in cleaned_items]]

        self._model.Add(
            comparison_func(*variables)
        )

    @property
    def added_items(self) -> Tuple:
        """
        The items that have been added, to the ranking problem
        :return:
        """
        return tuple([x for x in self._items if x not in POSITIONS])

    def set_items(self, items: list):
        if self._items != tuple():
            raise ValueError("Items Already Set")

        self._items = tuple([clean_variable(x) for x in items])
        self._reset_vars()

        return self

    def match_variable(self, item: str):
        if item not in POSITIONS:
            return fuzzy_match_variable(item, self._items)
        return item

    def add_item(self, item: str):
        new_item = self.match_variable(item)

        if new_item not in self._items:
            # calling self.reset will remove
            # previously added constraints
            # we only want to reset variables
            # self._variables.clear()
            self._items = self._items + (new_item,)
            self.addVariable(new_item)
            self._reset_vars()

        return self

    def remove_item(self, item: str):
        item_to_remove = self.match_variable(item)

        if item_to_remove in self._items:
            new_items = list(self._items)
            new_items.remove(item_to_remove)

            #self._variables.clear()
            del self._variables[item_to_remove]

            if (new_items is not None) and len(new_items) > 0:
                self._items = tuple(new_items)
            else:
                self._items = tuple()
            self._reset_vars()

        return self

    def check_item_present(self, item):
        check_item = self.match_variable(item)

        if check_item not in POSITIONS + list(self._items):
            raise ValueError(f"{item} not in Items")
        return True

    def not_equal(self, a: str, b: str):
        self.check_item_present(a)
        self.check_item_present(b)

        a_match = self.match_variable(a)
        b_match = self.match_variable(b)

        self._model.Add(self._variables[a_match] != self._variables[b_match])

        return self

    def is_equal(self, a: str, b: str):
        self.check_item_present(a)
        self.check_item_present(b)

        a_match = self.match_variable(a)
        b_match = self.match_variable(b)

        self._model.Add(self._variables[a_match] == self._variables[b_match])

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
        self.check_item_present(a)
        self.check_item_present(b)

        a_match = self.match_variable(a)
        b_match = self.match_variable(b)

        self._model.Add(self._variables[a_match] == self._variables[b_match] - 1)

        self._model.Add(self._variables[a_match] == self._variables[b_match] + 1)

        return self

    def is_before(self, a: str, b: str):
        self.check_item_present(a)
        self.check_item_present(b)

        a_match = self.match_variable(a)
        b_match = self.match_variable(b)

        self._model.Add(self._variables[a_match] < self._variables[b_match])

        return self

    def is_after(self, a: str, b: str):
        self.check_item_present(a)
        self.check_item_present(b)

        a_match = self.match_variable(a)
        b_match = self.match_variable(b)

        self._model.Add(self._variables[a_match] > self._variables[b_match])

        return self

    def is_just_before(self, a: int, b: int):
        self.check_item_present(a)
        self.check_item_present(b)

        self.add_rank_constraint(
            is_just_before, a, b, NEARBY
        )

        return self

    def is_just_after(self, a: int, b: int):
        self.check_item_present(a)
        self.check_item_present(b)

        self.add_rank_constraint(
            is_just_after, a, b, NEARBY
        )

        return self

    def is_nearby(self, a: int, b: int):
        self.check_item_present(a)
        self.check_item_present(b)

        self.add_rank_constraint(
            is_within_range, a, b, NEARBY
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
        solver = cp_model.CpSolver()
        solution_callback = RankingSolver([x for x in self._variables.values()])

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
        return {k: v for k, v in sorted(result.items(), key=lambda item: item[1])}

    @property
    def specified_constraints(self):
        return [x for x in self._model._CpModel__model.constraints if len(x.linear.vars)> 0]

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
