from copy import copy
from constraint import Problem
from constraint import AllDifferentConstraint
from .positions import FIRST, LAST
from .criteria import not_equal, not_directly_before, not_directly_after
from .criteria import is_before, is_after


class RankingProblem(Problem):

    def __init__(self):
        super().__init__()
        self._items = tuple()
        self._number_of_items = 0

    def _reset_vars(self):
        self._number_of_items = len(self._items)

        self.addVariable(FIRST, [0])
        self.addVariable(LAST, [self._number_of_items-1])

        self.addVariables(self._items, range(self._number_of_items))

        # given self._items might have changed update the
        # first constraint to consider the new set of self._items
        # otherwise we'd be adding redundant constraints
        if len(self._constraints) > 0:
            self._constraints[0] = (AllDifferentConstraint(), self._items)
        else:
            self.addConstraint(AllDifferentConstraint(), self._items)

    def add_rank_constraint(self, comparison_func, *items):
        cleaned_items = [self.clean_item(x) for x in items]

        self.addConstraint(
            comparison_func,
            tuple(cleaned_items)
        )

    def set_items(self, items: list):
        if self._items != tuple():
            raise ValueError("Items Already Set")

        self._items = tuple([self.clean_item(x) for x in items])
        self._reset_vars()

        return self

    def clean_item(self, item):
        new_item = copy(item)
        return new_item.replace("[", "").replace("]", "").strip().replace(" ", "_")

    def add_item(self, item: str):
        new_item = self.clean_item(item)

        if new_item not in self._items:
            # calling self.reset will remove
            # previously added constraints
            # we only want to reset variables
            self._variables.clear()
            self._items = self._items + (new_item,)
            self._reset_vars()

        return self

    def remove_item(self, item: str):
        new_item = self.clean_item(item)

        if new_item in self._items:
            new_items = list(self._items)
            new_items.remove(new_item)

            self._variables.clear()
            if (new_items is not None) and len(new_items) > 0:
                self._items = tuple(new_items)
            else:
                self._items = tuple()
            self._reset_vars()

        return self

    def check_item_present(self, item):
        check_item = self.clean_item(item)

        if check_item not in [FIRST, LAST] + list(self._items):
            raise ValueError(f"{item} not in Items")
        return True

    def not_equal(self, a: str, b: str):
        self.check_item_present(a)
        self.check_item_present(b)

        self.add_rank_constraint(
            not_equal, a, b
        )

        return self

    def not_last(self, item: str):
        self.not_equal(item, LAST)

        return self

    def not_first(self, item: str):
        self.not_equal(item, FIRST)

        return self

    def not_directly_before_or_after(self, a: str, b: str):
        self.check_item_present(a)
        self.check_item_present(b)

        self.add_rank_constraint(
            not_directly_before, a, b
        )

        self.add_rank_constraint(
            not_directly_after, a, b
        )

        return self

    def is_before(self, a: str, b: str):
        self.check_item_present(a)
        self.check_item_present(b)

        self.add_rank_constraint(
            is_before, a, b
        )

        return self

    def is_after(self, a: str, b: str):
        self.check_item_present(a)
        self.check_item_present(b)

        self.add_rank_constraint(
            is_after, a, b
        )

        return self

    def remove_last_constraint(self):
        if len(self._constraints) > 0:
            del self._constraints[-1]

        return self

    def number_of_constraints(self):
        return len(self._constraints)

    def solve(self):
        result = []
        solutions = self.getSolutions()

        for s in solutions:
            output = [""] * self._number_of_items
            for person, position in s.items():
                if person in self._items:
                    output[position] = person

            result.append(tuple(output))

        result.sort()
        return result
