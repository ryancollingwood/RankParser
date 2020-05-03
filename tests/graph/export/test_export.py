import os
import uuid
from solver import RankingParser
from graph import export_csv
from test_data import tea_steps, tea_steps_result_csv


def test_can_call_export_csv():
    try:
        export_csv()
    except TypeError:
        pass


def test_export_csv():
    test = RankingParser()

    filename = str(uuid.uuid1())
    filename = f"{filename}.csv"

    solutions = test.parse_statements(tea_steps, return_last_parsed = False)

    export_csv(solutions, filename)

    lines = None
    with open(filename, "r") as txt_file:
        lines = txt_file.readlines()

    assert("".join(lines) == tea_steps_result_csv)

    os.remove(filename)
