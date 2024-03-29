import uuid
import pprint
from os import mkdir
from shutil import move, copytree
from os import path
from colorama import Style
from prompt_toolkit import PromptSession
from prompt_toolkit.auto_suggest import AutoSuggestFromHistory
from prompt_toolkit.completion import WordCompleter

from solver import RankingParser, RankingLexer
from solver import IncompleteResultsError, UnsolvableModelError, ParsingError
from graph import RankingGraph
from graph import RankingNetwork
from interactive import HighLighter
from interactive import STYLE_MAP
from graph import generate_viz_from_solutions, export_csv, stats_from_solutions, export_highlighted_path
from input_output import export_lines_to_text, import_text_to_lines, check_file_extension
from .help import commands
from .printout import printout


class Session(object):

    def __init__(self, project_id=None, log_history=True):
        self.generated_project = True
        self.log_history = log_history
        self.project_id = None
        self.set_project_id(project_id)
        self._rp = None
        self.reset_ranking_parser()
        self._rl = RankingLexer()
        self._rg = RankingGraph()
        self._rn = RankingNetwork()
        self.lexer = self._rl.build()

        self._hl = HighLighter(self._rl, STYLE_MAP)
        self.history = list()
        self.pp = pprint.PrettyPrinter(indent=4)

    def reset_ranking_parser(self):
        self._rp = RankingParser()
        self._rp.build()

    def set_project_id(self, project_id):
        if project_id is not None:
            self.generated_project = False
            self.project_id = project_id
        else:
            self.project_id = str(uuid.uuid1())

    def change_project_id(self, project_id, move_files=True):
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
            self.reset_ranking_parser()

            self.generated_project = False
            self.set_project_id(project_id)
            self.load_history(project_id)

    def file_in_project(self, filename, extension="txt"):
        result = check_file_extension(filename, extension)
        if result[:len(self.project_id)] != self.project_id:
            result = f"{self.project_id}/{result}"

        return result

    def do_parse(self, text, write_history=True):
        if text.strip() == "":
            return

        print(self._hl.highlight(text))

        try:
            result = self._rp.parse(text)
        except ParsingError as e:
            print(STYLE_MAP["ERROR"], f"ERROR: {e}", STYLE_MAP["RESET"])
            return

        if result is not None:
            self.history.append(text)
            if write_history:
                self.write_history()

            if not self._rp.ranking_problem.is_solvable:
                self.undo()

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
            self.do_parse(l, write_history=False)

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
        if len(self.history) > 0:
            print(f"{STYLE_MAP['ERROR']}Undoing:{STYLE_MAP['RESET']}", self._hl.highlight(self.history[-1]))
            self._rp.remove_last_constraint()

    def print_history(self):
        for h in self.history:
            print(self._hl.highlight(h))

    def print_token_debug(self, s):
        self.do_tokenize(s.strip())

    def generate_graph(self, filename):
        solutions = self.solve()
        if len(solutions) == 0:
            print("No solutions to generate a graph from")
            return

        generate_viz_from_solutions(solutions, filename)

    def export_csv(self, filename):
        solutions = self.solve()
        if len(solutions) == 0:
            print("No solutions to generate a graph from")
            return

        output_filename = self.file_in_project(filename, "csv")
        export_csv(solutions, output_filename)

    def suggest_pair(self):
        pair = None

        try:
            pair = self._rp.ranking_problem.least_most_common_variable
        except Exception as e:
            print("Couldn't suggest pair", e)
            return

        print(self._hl.highlight(f"[{pair[0]}] versus [{pair[1]}]"))

    def solve(self):
        result = list()
        try:
            result = self._rp.solve()
        except IncompleteResultsError as e:
            print(f"{STYLE_MAP['ERROR']}{e.message}{Style.NORMAL}{STYLE_MAP['RESET']}")
            # result = e.results
        except UnsolvableModelError as e:
            print(f"{STYLE_MAP['ERROR']}{e.message}{Style.NORMAL}{STYLE_MAP['RESET']}")

        return result

    def print_stats(self, filename=None):
        solutions = self.solve()
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
            try:
                command_example = self._hl.highlight(commands[key][1])
            except ParsingError as e:
                command_example = commands[key][1]

            print(f"{Style.DIM}{command_example}{Style.NORMAL}")
            print()
        print(Style.RESET_ALL)

    def display_solution(self):
        result = self.solve()
        if len(result) == 1:
            self.pp.pprint(result[0])
        elif len(result) < 5:
            self.pp.pprint(result)
        else:
            print(f"{STYLE_MAP['INFO']}More than 5 results showing the path(s) with most support{STYLE_MAP['RESET']}")
            highlight_path = export_highlighted_path(result)
            self.pp.pprint(highlight_path)

    def read_input(self, text):
        text_split = text.split(" ")

        if text == "=":
            self.display_solution()
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

        prompt_session = PromptSession()
        word_completer = WordCompleter(self._rp.items, ignore_case=True)

        while True:
            prompt = "RankParser>"
            if not self.generated_project:
                prompt = f"{self.project_id}>"

            text = prompt_session.prompt(
                prompt, auto_suggest=AutoSuggestFromHistory(), completer=word_completer, complete_in_thread=True
            )

            if text.lower() == "quit":
                break

            if text != "":
                try:
                    self.read_input(text)
                except Exception as e:
                    print(Style.RESET_ALL)
                    print(f"{STYLE_MAP['ERROR']}Error reading input: {text}")
                    print(f"{e}{Style.NORMAL}")
                else:
                    word_completer.words = self._rp.items


if __name__ == "__main__":
    sess = Session()
    sess.start()
