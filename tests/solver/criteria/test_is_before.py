from solver.criteria import is_before


def test_can_call_is_before():
    is_before(1, 2)


def test_is_before_true():
    assert (is_before(1, 2))


def test_is_before_false():
    assert (not is_before(2, 1))


def test_is_before_equals():
    assert (not is_before(1, 1))

