from test_data import programmer_riddle
from interactive import Session


def test_can_call_session_do_parse():
    session = Session()
    session.do_parse(programmer_riddle[0])

def test_session_do_parse_empty():
    session = Session()
    session.do_parse("")

