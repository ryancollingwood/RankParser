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

    def set_items(self, items: list):
        if self._items != tuple():
            raise ValueError("Items Already Set")

        self._items = tuple(items.copy())
        self._reset_vars()

        return self

    def add_item(self, item: str):
        if item not in self._items:
            # calling self.reset will remove
            # previously added constraints
            # we only want to reset variables
            self._variables.clear()
            self._items = self._items + (item,)
            self._reset_vars()

    def check_item_present(self, item):
        if item not in [FIRST, LAST] + list(self._items):
            raise ValueError(f"{item} not in Items")
        return True

    def not_equal(self, a: str, b: str):
        self.check_item_present(a)
        self.check_item_present(b)

        self.addConstraint(
            not_equal,
            (a, b)
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

        self.addConstraint(
            not_directly_before,
            (a, b)
        )

        self.addConstraint(
            not_directly_after,
            (a, b)
        )

        return self

    def is_before(self, a: str, b: str):
        self.check_item_present(a)
        self.check_item_present(b)

        self.addConstraint(
            is_before,
            (a, b)
        )

        return self

    def is_after(self, a: str, b: str):
        self.check_item_present(a)
        self.check_item_present(b)

        self.addConstraint(
            is_after,
            (a, b)
        )

        return self

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
