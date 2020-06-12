from typing import List, Tuple, Dict
from itertools import chain
from statistics import stdev
from ortools.sat.python import cp_model
from .constraint_expression import ConstraintExpression
from .ranking_solver import RankingSolver
from .positions import FIRST, LAST, NEARBY, POSITIONS
from .variable_cleansor import clean_variable, fuzzy_match_variable


class RankingProblem:

    def __init__(self):
        super().__init__()
        self._model = cp_model.CpModel()
        self._results = list()
        self._variables = dict()
        self._items = tuple()
        self._constraints = list()
        self._nearby = 3

    def __add_variable(self, name: str, min_value: int = 0, max_value: int = None):
        """
        Add a variable, with the given range.

        :param name: str
        :param min_value: int - default 0
        :param max_value: int - default None
        :return:
        """
        self._variables[name] = (min_value, max_value)

    def __remove_variable(self, name: str):
        """
        Remove the given variable if present.

        :param name: str
        :return:
        """
        if name in self._variables:
            del self._variables[name]

        # TODO remove from constraints where items in name

    def __add_variables(self, names, min_value = 0, max_value = None):
        for name in names:
            self.__add_variable(name, min_value, max_value)

    def __reset_vars(self):
        """
        Reset the state of derived variables such as the `nearby_value`

        :return:
        """

        number_of_added_item = len(self.added_items)
        if number_of_added_item < 10:
            self._nearby = 3
        else:
            nearby_value = round(stdev(range(number_of_added_item)))
            self._nearby = nearby_value

    def __add_rank_constraint(self, comparison: str, *items):
        """
        Create a constraint expression to be applied when solving.

        :param comparison: str
        :param items:
        :return:
        """

        for item in items:
            self.check_item_present(item)

        cleaned_items = [self.match_variable(x) for x in items]

        new_constraint = ConstraintExpression(comparison, *cleaned_items)

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

    @property
    def number_of_items(self) -> int:
        """
        How many items have we have?

        :return:
        """
        return len(self._items)

    @property
    def number_of_constraints(self):
        """
        How many constraints have been specified
        :return:
        """
        return len(self._constraints)

    @property
    def variable_constraints_count(self) -> Dict[str, int]:
        """
        How many constraints does each variable participate in?

        :return: Dictionary of variable names with the number
            of constraints it participate in
        """
        result = self.item_links
        for item in result:
            result[item] = len(result[item])

        # return the result sorted by count
        return {k: v for k, v in sorted(result.items(), key=lambda sort_item: sort_item[1])}

    @property
    def specified_constraints(self):
        return [x for x in self._constraints]

    @property
    def item_links(self) -> Dict[str, List[str]]:
        """
        Detail the items an item is linked to via specified constraints.

        :return: Dict[str, List[str]]
        """
        result = dict()
        relevant_constraints = self.specified_constraints
        variables = self._variables

        for index, item in enumerate(variables):
            if item in POSITIONS:
                continue
            item_constraints = [x.items for x in relevant_constraints if item in x.items]
            item_links = set([x for x in list(chain(*item_constraints)) if x != item])
            result[item] = sorted(item_links)
        return {k: v for k, v in sorted(result.items(), key=lambda x: len(x[1]))}

    @property
    def least_most_common_variable(self) -> Tuple[str, str]:
        """
        Return a pair of variables where the first variable is the variable
        with least amount of links to other variables and the second is
        the variable with the greatest number of links, that does not include the
        first variable returned.

        :return: Tuple[str, str]
        """
        counts = self.variable_constraints_count
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

    def variable_domain(self, variable_name: str) -> Tuple[int, int]:
        """
        Return the domain of given domain.

        :param variable_name:
        :return:
        """
        return self._variables[variable_name]

    def set_items(self, items: list):
        """
        If no items have already been set, set the items to way is passed in.
        If items have already been set, a ValueError will be raised.

        :param items:
        :return:
        """
        if self._items != tuple():
            raise ValueError("Items Already Set")

        cleaned_items = [x for x in [clean_variable(item) for item in items] if x not in POSITIONS]

        self._items = tuple(cleaned_items)
        self.__add_variables(cleaned_items)

        return self

    def match_variable(self, item: str) -> str:
        """
        Look for the given item using fuzzy matching.
        If an Integer is passed, it is returned.

        :param item: str
        :return:
        """
        if isinstance(item, int):
            return item

        if item not in POSITIONS:
            return fuzzy_match_variable(item, tuple(self._variables.keys()))
        return item

    def add_item(self, item: str):
        """
        Add the given item (if not present or having a fuzzy match)
        to the variables.

        :param item: str
        :return:
        """
        new_item = self.match_variable(item)

        if new_item not in self._items:
            self._items = self._items + (new_item,)
            self.__add_variable(new_item)

        return self

    def remove_item(self, item: str):
        """
        Remove the given item (if present or having a fuzzy match)
        from the variables.

        :param item: str
        :return:
        """
        item_to_remove = self.match_variable(item)

        if item_to_remove in self._items:
            new_items = list(self._items)
            new_items.remove(item_to_remove)

            if (new_items is not None) and len(new_items) > 0:
                self._items = tuple(new_items)
            else:
                self._items = tuple()

            self.__remove_variable(item_to_remove)

        return self

    def check_item_present(self, item: str) -> bool:
        """
        Check if the given item has already present in our
        variables. If the item is an Integer then it will
        return True

        :param item:
        :return: bool
        """
        if isinstance(item, int):
            return True

        check_item = self.match_variable(item)

        if check_item not in POSITIONS + list(self._variables.keys()):
            raise ValueError(f"{item} not in Items")
        return True

    def not_equal(self, a: str, b: str):
        self.__add_rank_constraint(
            "{} != {}",
            a, b,
        )

        return self

    def is_equal(self, a: str, b: str):
        self.__add_rank_constraint(
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
        self.__add_rank_constraint(
            "{} != {} - 1",
            a, b
        )

        self.__add_rank_constraint(
            "{} != {} + 1",
            a, b
        )

        return self

    def is_before(self, a: str, b: str):
        self.__add_rank_constraint(
            "{} < {}",
            a, b
        )

        return self

    def is_after(self, a: str, b: str):
        self.__add_rank_constraint(
            "{} > {}",
            a, b
        )

        return self

    def is_just_before(self, a: int, b: int):
        self.__add_rank_constraint(
            "{} >= {} - {}",
            a, b, NEARBY
        )

        self.__add_rank_constraint(
            "{} < {}",
            a, b
        )
        return self

    def is_just_after(self, a: int, b: int):
        self.__add_rank_constraint(
            "{} <= {} + {}",
            a, b, NEARBY
        )

        self.__add_rank_constraint(
            "{} > {}",
            a, b
        )

        return self

    def is_nearby(self, a: int, b: int):

        self.__add_rank_constraint(
            "{} >= {} - {}",
            a, b, NEARBY
        )

        self.__add_rank_constraint(
            "{} <= {} + {}",
            a, b, NEARBY
        )

        return self

    def remove_last_constraint(self):
        """
        Remove the most recently added constraint

        :return:
        """
        if len(self._constraints) > 0:
            del self._constraints[-1]

        return self

    def solve(self) -> List[Tuple[str]]:
        """
        Solve the constraints and return the results.

        :return:
        """
        result = []

        self.__reset_vars()
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
            self._model.Add(eval(c.express("variables['{}']")))

        # exclude positions
        constraint_variables = [v for k, v in variables.items() if k not in POSITIONS]

        self._model.AddAllDifferent(constraint_variables)

        solver = cp_model.CpSolver()
        solution_callback = RankingSolver(constraint_variables)

        status = solver.Solve(self._model)
        if status in [cp_model.OPTIMAL, cp_model.FEASIBLE]:
            status = solver.SearchForAllSolutions(self._model, solution_callback)
        else:
            # TODO: give feedback on the status of the model
            print("Model isn't solvable")
            return list()

        result = solution_callback.results
        if not solution_callback.complete_results:
            print("Couldn't get complete results - specify more constraints")

        if len(result) == 0:
            return None

        result.sort()

        return result