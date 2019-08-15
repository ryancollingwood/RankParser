def distance_between(a, b):
    return b - a


def is_equal(a: int, b: int):
    return distance_between(a, b) == 0


def not_equal(a: int, b: int):
    return not is_equal(a, b)


def is_before(a: int, b: int):
    return distance_between(a, b) > 0


def is_after(a: int, b: int):
    if a == b:
        return False
    return not is_before(a, b)

