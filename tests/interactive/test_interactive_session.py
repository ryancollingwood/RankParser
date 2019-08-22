from test_data import programmer_riddle
from interactive import Session
from typing import List

def test_can_create_session():
    session = Session()
    assert(isinstance(session, Session))


def test_properties_set_on_create_session():
    session = Session()
    assert(isinstance(session.history, List))
    assert(len(session.history) == 0)

