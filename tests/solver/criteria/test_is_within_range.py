from solver.criteria import is_within_range


def test_can_call_is_within_range():
    is_within_range(1, 3, 2)


def test_is_with_range_below_correct():
    a = 10
    b = 15
    max_distance = 5

    assert(is_within_range(a, b, max_distance))


def test_is_with_range_above_correct():
    a = 15
    b = 10
    max_distance = 5

    assert(is_within_range(a, b, max_distance))


def test_is_with_range_below_incorrect():
    a = 10
    b = 15
    max_distance = 2

    assert(not is_within_range(a, b, max_distance))


def test_is_with_range_above_incorrect():
    a = 15
    b = 10
    max_distance = 2

    assert(not is_within_range(a, b, max_distance))
