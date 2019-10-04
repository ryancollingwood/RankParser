from test_data import programmer_riddle
from os import path
from interactive import Session
from typing import List
from shutil import rmtree


def test_can_create_session():
    session = Session()
    assert(isinstance(session, Session))


def test_properties_set_on_create_session():
    session = Session()
    assert(isinstance(session.history, List))
    assert(len(session.history) == 0)
    assert(isinstance(session.project_id, str))


def test_session_creates_history():
    session = Session()
    project_id = session.project_id

    for line in programmer_riddle:
        session.read_input(line)

    assert(path.exists(project_id))
    assert(path.exists(f"{project_id}/output.txt"))
    rmtree(project_id, True)


def test_session_does_not_create_history_when_told_no_logging():
    session = Session(log_history = False)
    project_id = session.project_id

    for line in programmer_riddle:
        session.read_input(line)

    assert(not path.exists(project_id))
