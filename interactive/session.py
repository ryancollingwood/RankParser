import pprint
from solver import RankingParser
from solver import RankingLexer
from interactive import HighLighter
from interactive import STYLE_MAP


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
        print(self._hl.highlight(text))

        result = self._rp.parse(text)

        if result is not None:
            self.history.append(text)

            if len(result) == 1:
                self.pp.pprint(result[0])
            elif len(result) > 1:
                self.pp.pprint(result)

    def do_tokenize(self, text):
        result = self._rl.tokenize(text.strip())
        self.pp.pprint(result)

    def read_input(self, text):
        if text == "undo":
            self._rp.remove_last_constraint()
            print(self._rp.solve())
        elif text == "history":
            for h in self.history:
                print(self._hl.highlight(h))
        else:
            if len(text) > 2 and text[0] == "?":
                self.do_tokenize(text[1:].strip())
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
