from copy import copy
import re
from interactive.style_map import STYLE_MAP
from solver import RankingLexer
from colorama import Fore, Style
from colorama import init as colorama_init
from test_data import programmer_riddle


class HighLighter(object):

    def __init__(self, lexer, style_map):
        self.lexer = lexer
        self.style_map = style_map

    def highlight(self, text):
        result = copy(text)

        rl = RankingLexer()
        tokens = rl.tokenize(text)

        replacements = dict()

        for t in tokens:
            if t.type not in self.style_map:
                continue

            if t.value in replacements:
                continue

            replacement = self.style_map[t.type] + t.value + Fore.RESET + Style.NORMAL
            replacements[t.value] = replacement

        for r in replacements:
            result = re.sub(f"\\b{r}\\b", replacements[r], result)

        return result


def test_highlighter():
    colorama_init()
    hl = HighLighter(RankingLexer(), STYLE_MAP)

    # this will create a text file of the escaped terminal
    # colour codes included too
    with open("highlight_out.txt", "w") as f:
        for s in programmer_riddle:
            s_out = hl.highlight(s)
            f.write(s_out+"\n")
            print(s_out)
        f.close()


if __name__ == "__main__":
    test_highlighter()
