import pprint
from solver import RankingParser, RankingLexer
from interactive import HighLighter
from interactive import STYLE_MAP
from graph import generate_viz_from_solutions


class Session(object):

    def __init__(self):
        self._rp = RankingParser()
        self._rl = RankingLexer()
        self.lexer = self._rl.build()
        self._rp.build()
        self._hl = HighLighter(self._rl, STYLE_MAP)
        self.history = list()
        self.pp = pprint.PrettyPrinter(indent=4)

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
            file_name = "output.txt"

            with open(file_name, "w") as f:
                for l in self.history:
                    f.write(f"{l}\n")
        except:
            pass

    def load_history(self):
        # TODO not hard coded file

        file_name = "output.txt"
        lines = []

        with open(file_name, "r") as f:
            lines = f.readlines()

        if len(lines) == 0:
            print(f"Nothing to read from {file_name}")
            return

        self.history.clear()

        for l in lines:
            self.do_parse(l)

    def import_items(self):
        # TODO not hard coded file

        file_name = "import_items.txt"

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
            self.import_items()
        elif text == "load":
            self.load_history()
        elif text_split[0] in ["graph", "diagram"]:
            if len(text_split) > 1:
                self.generate_graph(text_split[1])
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
            text = input("RankParser> ").strip()
            if text.lower() == "quit":
                break

            if text != "":
                self.read_input(text)


if __name__ == "__main__":
    sess = Session()
    sess.start()
