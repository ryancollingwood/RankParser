from solver.criteria import not_directly_before


def test_can_call_directly_before():
    not_directly_before(1, 2)


def test_directly_before_correct():
    assert(not_directly_before(2, 1))


def test_directly_before_incorrect():
    assert(not not_directly_before(1, 2))


def test_directly_before_zero():
    assert(not_directly_before(1, 1))



