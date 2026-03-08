class ConstraintExpression:

    def __init__(self, expression: str, *items):
        self.expression = expression
        self.items = items

    def __str__(self) -> str:
        return self.expression.format(*self.items)

    def __repr__(self) -> str:
        return self.__str__()

    def express(self, decorator: str = 'variables[{}]') -> str:
        variable_items = list()
        for item in self.items:
            if isinstance(item, int):
                variable_items.append(item)
            else:
                variable_items.append(decorator.format(item))

        return self.expression.format(*variable_items)

    def __contains__(self, item: str) -> bool:
        return item in self.items

