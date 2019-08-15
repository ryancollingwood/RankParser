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
        self.addVariable(FIRST, [0])

    def set_items(self, items: tuple):
        if self._items != tuple():
            raise ValueError("Items Already Set")

        self._items = items.copy()
        self._number_of_items = len(self._items)
        self.addVariable(LAST, [self._number_of_items-1])
        self.addConstraint(AllDifferentConstraint(), self._items)

        self.addVariables(self._items, range(self._number_of_items))

    def check_item_present(self, item):
        if item not in [FIRST, LAST] + list(self._items):
            raise ValueError(f"{item} not in Items")

    def not_equal(self, a: str, b: str):
        self.check_item_present(a)
        self.check_item_present(b)

        self.addConstraint(
            not_equal,
            (a, b)
        )

    def not_last(self, item: str):
        self.not_equal(item, LAST)

    def not_first(self, item: str):
        self.not_equal(item, FIRST)

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

    def is_before(self, a: str, b: str):
        self.check_item_present(a)
        self.check_item_present(b)

        self.addConstraint(
            is_before,
            (a, b)
        )

    def is_after(self, a: str, b: str):
        self.check_item_present(a)
        self.check_item_present(b)

        self.addConstraint(
            is_after,
            (a, b)
        )
