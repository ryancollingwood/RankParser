import uuid
from os import mkdir
from shutil import move, copytree
from os import path

from solver import RankingParser, RankingLexer
from solver import IncompleteResultsError, UnsolvableModelError, ParsingError
from graph import generate_viz_from_solutions, export_csv, stats_from_solutions, export_highlighted_path
from input_output import export_lines_to_text, import_text_to_lines, check_file_extension

class RankParserCore(object):
    def __init__(self, project_id: str = None, log_history: bool = True) -> None:
        self.generated_project = True
        self.log_history = log_history
        self.project_id = None
        self.set_project_id(project_id)
        self._rp = None
        self.reset_ranking_parser()
        self._rl = RankingLexer()
        self.lexer = self._rl.build()
        self.history = list()

    def reset_ranking_parser(self) -> None:
        self._rp = RankingParser()
        self._rp.build()

    def set_project_id(self, project_id: str) -> None:
        if project_id is not None:
            self.generated_project = False
            self.project_id = project_id
        else:
            self.project_id = str(uuid.uuid1())

    def change_project_id(self, project_id: str, move_files: bool = True) -> None:
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

    def file_in_project(self, filename: str, extension: str = "txt") -> str:
        result = check_file_extension(filename, extension)
        if result[:len(self.project_id)] != self.project_id:
            result = f"{self.project_id}/{result}"

        return result

    def do_parse(self, text: str, write_history: bool = True):
        """Parses the text, updates history, and returns the result."""
        if text.strip() == "":
            return None

        result = self._rp.parse(text)

        if result is not None:
            self.history.append(text)
            if write_history:
                self.write_history()

            if not self._rp.ranking_problem.is_solvable:
                self.undo()
                if write_history:
                    self.write_history()
                raise UnsolvableModelError("Model is not solvable after applying constraint")

        return result

    def write_history(self) -> None:
        if not self.log_history:
            return

        try:
            if not path.exists(self.project_id):
                mkdir(self.project_id)

            file_name = self.file_in_project("output", "txt")

            export_lines_to_text(self.history, file_name)
        except:
            pass

    def load_history(self, project_id: str) -> int:
        file_name = f"{project_id}/output.txt"
        lines = import_text_to_lines(file_name)

        if len(lines) == 0:
            return 0

        self.history.clear()

        for l in lines:
            self.do_parse(l, write_history=False)

        return len(lines)

    def import_items(self, file_name: str) -> int:
        lines = import_text_to_lines(file_name)

        if len(lines) == 0:
            return 0

        for l in lines:
            self.do_parse(f"+ [{l.strip()}]")

        return len(lines)

    def export_items(self, file_name: str) -> str:
        output_file_name = self.file_in_project(file_name, "txt")
        export_lines_to_text(self._rp.items, output_file_name)
        return output_file_name

    def do_tokenize(self, text: str) -> list:
        return self._rl.tokenize(text.strip())

    def undo(self) -> str:
        if len(self.history) > 0:
            last_cmd = self.history.pop()
            self._rp.remove_last_constraint()
            return last_cmd
        return None

    def get_history(self) -> list:
        return self.history

    def generate_graph(self, filename: str) -> str:
        solutions = self.solve()
        if len(solutions) == 0:
            return None
        generate_viz_from_solutions(solutions, filename)
        return filename

    def export_csv(self, filename: str) -> str:
        solutions = self.solve()
        if len(solutions) == 0:
            return None

        output_filename = self.file_in_project(filename, "csv")
        export_csv(solutions, output_filename)
        return output_filename

    def suggest_pair(self) -> tuple:
        return self._rp.ranking_problem.least_most_common_variable

    def solve(self) -> list:
        return self._rp.solve()

    def get_stats(self, filename: str = None) -> dict:
        solutions = self.solve()
        if len(solutions) == 0:
            return None

        result = stats_from_solutions(solutions)

        if filename is not None:
            lines = list()
            for key in result:
                lines.append(f"{key}={result[key]}")
            export_lines_to_text(lines, self.file_in_project(filename))

        return result

    def get_items(self) -> list:
        return self._rp.items
