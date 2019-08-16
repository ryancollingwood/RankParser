from solver.criteria import not_equal


def test_can_call_not_equal():
    not_equal(1, 2)


def test_not_equal_true():
    assert(not_equal(1, 2))


def test_not_equal_false():
    assert(not not_equal(1, 1))

