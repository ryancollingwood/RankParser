from solver.criteria import not_directly_after


def test_can_call_directly_after():
    not_directly_after(1, 2)


def test_directly_after_correct():
    assert(not_directly_after(1, 2))


def test_directly_after_incorrect():
    assert(not not_directly_after(2, 1))


def test_directly_after_zero():
    assert(not_directly_after(1, 1))



