def is_before(a: int, b: int):
    return a < b


def not_equal(a: int, b: int):
    return a != b


def is_after(a: int, b: int):
    if a == b:
        return False
    return not is_before(a, b)
