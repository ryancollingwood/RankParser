import pprint
from colorama import Style
from prompt_toolkit import PromptSession
from prompt_toolkit.auto_suggest import AutoSuggestFromHistory
from prompt_toolkit.completion import WordCompleter

from solver import IncompleteResultsError, UnsolvableModelError, ParsingError
from interactive.highlight import HighLighter
from interactive.style_map import STYLE_MAP
from interactive.core import RankParserCore
from graph import export_highlighted_path
from .help import commands
from .printout import printout


class Session(object):

    def __init__(self, project_id: str = None, log_history: bool = True) -> None:
        self.core = RankParserCore(project_id, log_history)
        self._hl = HighLighter(self.core._rl, STYLE_MAP)
        self.pp = pprint.PrettyPrinter(indent=4)

    @property
    def project_id(self):
        return self.core.project_id

    @property
    def history(self):
        return self.core.history

    def change_project_id(self, project_id: str, move_files: bool = True) -> None:
        self.core.change_project_id(project_id, move_files)

    def do_parse(self, text: str, write_history: bool = True) -> None:
        if text.strip() == "":
            return

        print(self._hl.highlight(text))

        try:
            self.core.do_parse(text, write_history)
        except ParsingError as e:
            print(STYLE_MAP["ERROR"], f"ERROR: {e}", STYLE_MAP["RESET"])
        except UnsolvableModelError:
            print(f"{STYLE_MAP['ERROR']}Undoing:{STYLE_MAP['RESET']}", self._hl.highlight(text))

    def write_history(self) -> None:
        self.core.write_history()

    def load_history(self, project_id: str) -> None:
        lines_read = self.core.load_history(project_id)
        if lines_read == 0:
            print(f"Nothing to read from {project_id}/output.txt")

    def import_items(self, file_name: str) -> None:
        lines_read = self.core.import_items(file_name)
        if lines_read == 0:
            print(f"Nothing to read from {file_name}")
        else:
            print("imported items")

    def export_items(self, file_name: str) -> None:
        output_file_name = self.core.export_items(file_name)
        print(f"exported items to {output_file_name}")

    def do_tokenize(self, text: str) -> None:
        result = self.core.do_tokenize(text)
        self.pp.pprint(result)

    def undo(self) -> None:
        last_cmd = self.core.undo()
        if last_cmd is not None:
            print(f"{STYLE_MAP['ERROR']}Undoing:{STYLE_MAP['RESET']}", self._hl.highlight(last_cmd))

    def print_history(self) -> None:
        for h in self.core.get_history():
            print(self._hl.highlight(h))

    def print_token_debug(self, s: str) -> None:
        self.do_tokenize(s.strip())

    def generate_graph(self, filename: str) -> None:
        result = self.core.generate_graph(filename)
        if result is None:
            print("No solutions to generate a graph from")

    def export_csv(self, filename: str) -> None:
        result = self.core.export_csv(filename)
        if result is None:
            print("No solutions to generate a graph from")

    def suggest_pair(self) -> None:
        try:
            pair = self.core.suggest_pair()
            print(self._hl.highlight(f"[{pair[0]}] versus [{pair[1]}]"))
        except Exception as e:
            print("Couldn't suggest pair", e)

    def solve(self) -> list:
        result = list()
        try:
            result = self.core.solve()
        except IncompleteResultsError as e:
            print(f"{STYLE_MAP['ERROR']}{e.message}{Style.NORMAL}{STYLE_MAP['RESET']}")
            # result = e.results
        except UnsolvableModelError as e:
            print(f"{STYLE_MAP['ERROR']}{e.message}{Style.NORMAL}{STYLE_MAP['RESET']}")

        return result

    def print_stats(self, filename: str = None) -> None:
        result = self.core.get_stats(filename)
        if result is None:
            print("No solutions to generate a stats from")
            return

        print(Style.RESET_ALL)

        for item in result:
            print(f"{Style.BRIGHT}{item}{Style.NORMAL}")
            printout(result[item], item)

        print(Style.RESET_ALL)

    def display_commands(self) -> None:
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

    def display_solution(self) -> None:
        result = self.solve()
        if len(result) == 1:
            self.pp.pprint(result[0])
        elif len(result) < 5:
            self.pp.pprint(result)
        else:
            print(f"{STYLE_MAP['INFO']}More than 5 results showing the path(s) with most support{STYLE_MAP['RESET']}")
            highlight_path = export_highlighted_path(result)
            self.pp.pprint(highlight_path)

    def read_input(self, text: str) -> None:
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
                self.generate_graph(f"{self.core.project_id}/{text_split[1]}")
            else:
                print("Need to specify a filename")
        elif text_split[0] in ["csv"]:
            if len(text_split) > 1:
                self.export_csv(f"{self.core.project_id}/{text_split[1]}")
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

    def start(self) -> None:

        prompt_session = PromptSession()
        word_completer = WordCompleter(self.core.get_items(), ignore_case=True)

        while True:
            prompt = "RankParser>"
            if not self.core.generated_project:
                prompt = f"{self.core.project_id}>"

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
                    word_completer.words = self.core.get_items()


if __name__ == "__main__":
    sess = Session()
    sess.start()
