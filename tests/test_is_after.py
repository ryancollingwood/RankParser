from solver.criteria import is_after

def test_can_call_is_after():
    is_after(2, 1)


def test_is_after_correct():
    assert(is_after(2,1))


def test_is_after_incorrect():
    assert(not is_after(1,2))

def test_is_after_equals():
    assert(not is_after(1,1))

