from solver.criteria import distance_between


def test_can_call_distance_between():
    distance_between(1, 2)


def test_distance_between_zero():
    assert(distance_between(1, 1) == 0)


def test_distance_between_positive():
    assert(distance_between(1, 2) > 0)


def test_distance_between_negative():
    assert(distance_between(2, 1) < 0)

