from solver.criteria import directly_after


def test_can_call_directly_after():
    directly_after(2, 1)


def test_directly_after_correct():
    assert(directly_after(2, 1))


def test_directly_after_incorrect():
    assert(not directly_after(1,2))


def test_directly_after_zero():
    assert(not directly_after(1, 1))
