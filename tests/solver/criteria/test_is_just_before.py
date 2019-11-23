from solver.criteria import is_just_before


def test_can_call_is_just_before():
    is_just_before(4, 7, 2)


def test_is_just_before_correct():
    a = 5
    b = 7
    max_distance = 3

    assert(is_just_before(a, b, max_distance))


def test_is_just_before_out_of_max_distance():
    a = 10
    b = 20
    max_distance = 5

    assert(not is_just_before(a, b, max_distance))


def test_is_just_before_not_before():
    a = 9
    b = 8
    max_distance = 3

    assert(not is_just_before(a, b, max_distance))

