from solver.criteria import is_equal


def test_can_call_is_equal():
    is_equal(1, 2)


def test_is_equal_correct():
    assert(is_equal(1, 1))


def test_is_equal_incorrect():
    assert(not is_equal(1, 2))

