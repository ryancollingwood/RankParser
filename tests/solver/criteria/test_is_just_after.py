from solver.criteria import is_just_after


def test_can_call_is_just_after():
    is_just_after(4, 7, 2)


def test_is_just_after_correct():
    a = 7
    b = 5
    max_distance = 3

    assert(is_just_after(a, b, max_distance))


def test_is_just_after_out_of_max_distance():
    a = 20
    b = 10
    max_distance = 5

    assert(not is_just_after(a, b, max_distance))


def test_is_just_after_not_after():
    a = 3
    b = 5
    max_distance = 3

    assert(not is_just_after(a, b, max_distance))

