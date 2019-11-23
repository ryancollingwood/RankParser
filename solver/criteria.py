def distance_between(a, b):
    return b - a


def is_equal(a: int, b: int):
    return distance_between(a, b) == 0


def not_equal(a: int, b: int):
    return not is_equal(a, b)


def is_before(a: int, b: int):
    return distance_between(a, b) > 0


def is_just_before(a: int, b: int, max_distance: int):

    if is_before(a, b):
        distance = distance_between(a, b)
        return distance <= max_distance

    return False


def is_after(a: int, b: int):
    if a == b:
        return False
    return not is_before(a, b)


def is_just_after(a: int, b: int, max_distance: int):
    if is_after(a, b):
        distance = distance_between(a, b)
        return abs(distance) <= max_distance

    return False


def is_within_range(a: int, b: int, max_distance: int):
    return abs(distance_between(a, b)) <= max_distance


def directly_before(a: int, b: int):
    distance = distance_between(a, b)
    return distance == 1


def directly_after(a: int, b: int):
    distance = distance_between(a, b)
    return distance == -1


def not_directly_before(a: int, b: int):
    return not directly_before(a, b)


def not_directly_after(a: int, b: int):
    return not directly_after(a, b)
