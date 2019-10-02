import uuid
import pprint
from os import mkdir
from shutil import move
from os import path
from solver import RankingParser, RankingLexer
from interactive import HighLighter
from interactive import STYLE_MAP
from graph import generate_viz_from_solutions


class Session(object):

    def __init__(self, session_id = None):
        self.generated_session = True
        self.session_id = self.set_session_id(session_id)
        self._rp = RankingParser()
        self._rl = RankingLexer()
        self.lexer = self._rl.build()
        self._rp.build()
        self._hl = HighLighter(self._rl, STYLE_MAP)
        self.history = list()
        self.pp = pprint.PrettyPrinter(indent=4)

    def set_session_id(self, session_id):
        if session_id is not None:
            self.generated_session = False
            return session_id
        return str(uuid.uuid1())

    def change_session_id(self, session_id):
        self.generated_session = False

        if not path.exists(session_id):
            move(self.session_id, session_id)
            self.set_session_id(session_id)
        else:
            self.set_session_id(session_id)
            self.load_history(session_id)


    def do_parse(self, text):
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

            self.write_history()

    def write_history(self):
        try:
            mkdir(self.session_id)
            file_name = f"{self.session_id}/output.txt"

            with open(file_name, "w") as f:
                for l in self.history:
                    f.write(f"{l}\n")
        except:
            pass

    def load_history(self, session_id):
        file_name = f"{session_id}/output.txt"
        lines = []

        with open(file_name, "r") as f:
            lines = f.readlines()

        if len(lines) == 0:
            print(f"Nothing to read from {file_name}")
            return

        self.history.clear()

        for l in lines:
            self.do_parse(l)

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
                self.change_session_id(text_split[1])
            else:
                print("Need to specify a filename")
        elif text_split[0] in ["graph", "diagram"]:
            if len(text_split) > 1:
                self.generate_graph(f"{self.session_id}/{text_split[1]}")
            else:
                print("Need to specify a filename")
        else:
            if len(text) > 2 and text[0] == "?":
                self.print_token_debug(text[1:])
            else:
                self.do_parse(text)

    def start(self):
        self._rp.build()

        while True:
            prompt = "RankParser>"
            if not self.generated_session:
                prompt = f"{self.session_id}>"

            text = input(prompt).strip()
            if text.lower() == "quit":
                break

            if text != "":
                self.read_input(text)


if __name__ == "__main__":
    sess = Session()
    sess.start()
