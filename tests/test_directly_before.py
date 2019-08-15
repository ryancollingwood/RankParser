from solver.criteria import directly_before


def test_can_call_directly_before():
    directly_before(1, 2)


def test_directly_before_correct():
    assert(directly_before(1, 2))


def test_directly_before_incorrect():
    assert(not directly_before(2, 1))


def test_directly_before_zero():
    assert(not directly_before(1, 1))



