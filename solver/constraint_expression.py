class ConstraintExpression:

    def __init__(self, expression, *items):
        self.expression = expression
        self.items = items

    def __str__(self):
        return self.expression.format(*self.items)

    def __repr__(self):
        return self.__str__()

    def express(self, decorator = 'variables[{}]'):
        variable_items = list()
        for item in self.items:
            if isinstance(item, int):
                variable_items.append(item)
            else:
                variable_items.append(decorator.format(item))

        return self.expression.format(*variable_items)
