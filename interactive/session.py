from collections import Iterable
import uuid
import pprint
from os import mkdir
from shutil import move, copytree
from os import path
from colorama import Style
from solver import RankingParser, RankingLexer
from graph import RankingGraph
from graph import RankingNetwork
from interactive import HighLighter
from interactive import STYLE_MAP
from graph import generate_viz_from_solutions, export_csv, stats_from_solutions
from input_output import export_lines_to_text, import_text_to_lines, check_file_extension
from .help import commands
from .printout import printout


class Session(object):

    def __init__(self, project_id = None, log_history = True):
        self.generated_project = True
        self.log_history = log_history
        self.project_id = None
        self.set_project_id(project_id)
        self._rp = RankingParser()
        self._rl = RankingLexer()
        self._rg = RankingGraph()
        self._rn = RankingNetwork()
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

    def change_project_id(self, project_id, move_files = True):
        if self.project_id == project_id:
            return

        if not path.exists(project_id):
            if self.generated_project or move_files:
                if path.exists(self.project_id):
                    move(self.project_id, project_id)
                else:
                    mkdir(project_id)
            else:
                if path.exists(self.project_id):
                    copytree(self.project_id, project_id)
                else:
                    mkdir(project_id)

            self.generated_project = False
            self.set_project_id(project_id)
        else:
            self.generated_project = False
            self.set_project_id(project_id)
            self.load_history(project_id)

    def file_in_project(self, filename, extension = "txt"):
        output_filename = check_file_extension(filename, extension)
        return f"{self.project_id}/{output_filename}"

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

            file_name = self.file_in_project("output", "txt")

            export_lines_to_text(self.history, file_name)
        except:
            pass

    def load_history(self, project_id):
        file_name = f"{project_id}/output.txt"
        lines = import_text_to_lines(file_name)

        if len(lines) == 0:
            print(f"Nothing to read from {file_name}")
            return

        self.history.clear()

        for l in lines:
            self.do_parse(l, write_history= False)

    def import_items(self, file_name):
        lines = import_text_to_lines(file_name)

        if len(lines) == 0:
            print(f"Nothing to read from {file_name}")
            return

        for l in lines:
            self.do_parse(f"+ [{l.strip()}]")

        print("imported items")

    def export_items(self, file_name):
        output_file_name = self.file_in_project(file_name, "txt")
        export_lines_to_text(self._rp.items, output_file_name)
        print(f"exported items to {output_file_name}")

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

        output_filename = self.file_in_project(filename, "csv")
        export_csv(solutions, output_filename)

    def suggest_pair(self):
        pair = None

        try:
            pair = self._rp.ranking_problem.least_most_common_variable()
        except Exception as e:
            print("Couldn't suggest pair", e)
            return

        print(self._hl.highlight(f"[{pair[0]}] versus [{pair[1]}]"))

    def print_stats(self, filename = None):
        solutions = self._rp.solve()
        if len(solutions) == 0:
            print("No solutions to generate a stats from")
            return

        result = stats_from_solutions(solutions)
        print(Style.RESET_ALL)

        for item in result:
            print(f"{Style.BRIGHT}{item}{Style.NORMAL}")
            printout(result[item], item)

        print(Style.RESET_ALL)

        if filename is not None:
            lines = list()
            for key in result:
                lines.append(f"{key}={result[key]}")
            export_lines_to_text(lines, self.file_in_project(filename))

    def display_commands(self):
        for key in commands:
            print(Style.RESET_ALL)
            print(f"{Style.BRIGHT}{key}{Style.NORMAL} : {commands[key][0]}")
            print(self._hl.highlight(commands[key][1]))
            print()
        print(Style.RESET_ALL)

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
        elif text_split[0] in ["import_items", "import"]:
            if len(text_split) > 1:
                self.import_items(text_split[1])
            else:
                print("Need to specify a filename")
        elif text_split[0] in ["export_items", "export"]:
            if len(text_split) > 1:
                self.export_items(text_split[1])
            else:
                print("Need to specify a filename")
        elif text_split[0] == "load":
            if len(text_split) > 1:
                self.change_project_id(text_split[1])
            else:
                print("Need to specify a filename")
        elif text_split[0] == "copy":
            if len(text_split) > 1:
                self.change_project_id(text_split[1], move_files=False)
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
        elif text_split[0] in ["stats"]:
            if len(text_split) > 1:
                self.print_stats(text_split[1])
            else:
                self.print_stats()
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
