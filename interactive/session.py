import uuid
import pprint
from os import mkdir
from shutil import move
from os import path
from solver import RankingParser, RankingLexer
from interactive import HighLighter
from interactive import STYLE_MAP
from graph import generate_viz_from_solutions, export_csv
from .help import commands


class Session(object):

    def __init__(self, project_id = None, log_history = True):
        self.generated_project = True
        self.log_history = log_history
        self.project_id = None
        self.set_project_id(project_id)
        self._rp = RankingParser()
        self._rl = RankingLexer()
        self.lexer = self._rl.build()
        self._rp.build()
        self._hl = HighLighter(self._rl, STYLE_MAP)
        self.history = list()
        self.pp = pprint.PrettyPrinter(indent=4)

    def set_project_id(self, project_id):
        if project_id is not None:
            self.generated_project = False
            self.project_id = project_id
        else:
            self.project_id = str(uuid.uuid1())

    def change_project_id(self, project_id):
        self.generated_project = False

        if not path.exists(project_id):
            move(self.project_id, project_id)
            self.set_project_id(project_id)
        else:
            self.set_project_id(project_id)
            self.load_history(project_id)

    def do_parse(self, text, write_history = True):
        if text.strip() == "":
            return

        print(self._hl.highlight(text))

        try:
            result = self._rp.parse(text)
        except TypeError as e:
            print(e)
            return

        if result is not None:
            self.history.append(text)
            if write_history:
                self.write_history()

    def write_history(self):
        if not self.log_history:
            return

        try:
            if not path.exists(self.project_id):
                mkdir(self.project_id)

            file_name = f"{self.project_id}/output.txt"

            with open(file_name, "w") as f:
                for l in self.history:
                    f.write(f"{l}\n")
        except:
            pass

    def load_history(self, project_id):
        file_name = f"{project_id}/output.txt"
        lines = []

        with open(file_name, "r") as f:
            lines = f.readlines()

        if len(lines) == 0:
            print(f"Nothing to read from {file_name}")
            return

        self.history.clear()

        for l in lines:
            self.do_parse(l, write_history= False)

    def import_items(self, file_name):

        with open(file_name, "r") as f:
            lines = f.readlines()

        if len(lines) == 0:
            print(f"Nothing to read from {file_name}")
            return

        for l in lines:
            self.do_parse(f"+ [{l.strip()}]")

        print("imported items")

    def do_tokenize(self, text):
        result = self._rl.tokenize(text.strip())
        self.pp.pprint(result)

    def undo(self):
        self._rp.remove_last_constraint()
        print(self._rp.solve())

    def print_history(self):
        for h in self.history:
            print(self._hl.highlight(h))

    def print_token_debug(self, s):
        self.do_tokenize(s.strip())

    def generate_graph(self, filename):
        solutions = self._rp.solve()
        if len(solutions) == 0:
            print("No solutions to generate a graph from")
            return

        generate_viz_from_solutions(solutions, filename)

    def export_csv(self, filename):
        solutions = self._rp.solve()
        if len(solutions) == 0:
            print("No solutions to generate a graph from")
            return

        export_csv(solutions, filename)

    def suggest_pair(self):
        pair = None

        try:
            pair = self._rp.ranking_problem.least_most_common_variable()
        except Exception as e:
            print("Couldnt suggest pair", e)
            return

        print(self._hl.highlight(f"[{pair[0]}] versus [{pair[1]}]"))

    def display_commands(self):
        for key in commands:
            print(f"{key} : {commands[key][0]}")
            print(self._hl.highlight(commands[key][1]))

            try:
                self.do_tokenize(commands[key][1])
            except:
                pass
            print()

    def read_input(self, text):
        text_split = text.split(" ")

        if text == "=":
            result = self._rp.solve()
            if len(result) == 1:
                self.pp.pprint(result[0])
            elif len(result) > 1:
                self.pp.pprint(result)
        elif text == "undo":
            self.undo()
        elif text == "history":
            self.print_history()
        elif text == "import_items":
            if len(text_split) > 1:
                self.import_items(text_split[1])
            else:
                print("Need to specify a filename")
        elif text_split[0] == "load":
            if len(text_split) > 1:
                self.change_project_id(text_split[1])
            else:
                print("Need to specify a filename")
        elif text_split[0] in ["graph", "diagram"]:
            if len(text_split) > 1:
                self.generate_graph(f"{self.project_id}/{text_split[1]}")
            else:
                print("Need to specify a filename")
        elif text_split[0] in ["csv"]:
            if len(text_split) > 1:
                self.export_csv(f"{self.project_id}/{text_split[1]}")
            else:
                print("Need to specify a filename")
        elif text_split[0] == "~":
            self.suggest_pair()
        elif text[0] == "?":
            if len(text) > 2:
                self.print_token_debug(text[1:].strip())
            else:
                print("insufficient parameters")
        elif text_split[0] == "help":
            self.display_commands()
        else:
            self.do_parse(text)

    def start(self):
        self._rp.build()

        while True:
            prompt = "RankParser>"
            if not self.generated_project:
                prompt = f"{self.project_id}>"

            text = input(prompt).strip()
            if text.lower() == "quit":
                break

            if text != "":
                try:
                    self.read_input(text)
                except Exception as e:
                    print(f"Error reading input: {text}")
                    print(e)


if __name__ == "__main__":
    sess = Session()
    sess.start()
