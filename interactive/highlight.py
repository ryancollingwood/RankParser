from copy import copy
import re
from interactive.style_map import STYLE_MAP
from solver import RankingLexer
from colorama import Fore, Back, Style
from colorama import init as colorama_init
from test_data import programmer_riddle


class HighLighter(object):

    def __init__(self, lexer, style_map):
        self.lexer = lexer
        self.style_map = style_map

    def highlight(self, text):
        result = copy(text)
        tokens = None
        rl = RankingLexer()

        try:
            tokens = rl.tokenize(text)
        except TypeError:
            return result

        replacements = dict()

        for t in tokens:
            if t.type not in self.style_map:
                continue

            if t.value in replacements:
                continue

            replacement = self.style_map[t.type] + \
                          t.value + \
                          Fore.RESET + \
                          Style.NORMAL + \
                          Back.RESET

            replacements[t.value] = replacement

        for r in replacements:
            escaped_r = re.escape(r)
            if r[0] != "[":
                result = re.sub(f"\\b{escaped_r}\\b", replacements[r], result)
            else:
                result = re.sub(f"{escaped_r}", replacements[r], result)

        return result


def test_write_out_highlighted_lines(file_name, lines):
    colorama_init()
    hl = HighLighter(RankingLexer(), STYLE_MAP)

    # this will create a text file of the escaped terminal
    # colour codes included too
    with open(file_name, "w") as f:
        for s in lines:
            s_out = hl.highlight(s)
            f.write(s_out+"\n")
            print(s_out)
        f.close()


def test_highlighter():
    test_write_out_highlighted_lines(
        "highlight_out.txt", programmer_riddle
    )


def complex_lines():
    return [
        "[Ryan (1)] before [(Other)]",
        "[Sue & Julie] before [Ryan (1)]",
        "[^Alfred^] not last",
    ]


def test_complex():

    test_write_out_highlighted_lines(
        "highlight_out_complex.txt", complex_lines()
    )


if __name__ == "__main__":
    test_highlighter()
    test_complex()

