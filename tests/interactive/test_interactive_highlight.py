from copy import copy
from interactive import HighLighter
from interactive import STYLE_MAP
from solver import RankingLexer
from test_data import programmer_riddle


def test_can_create_highlighter():
    hl = HighLighter(None, None)
    assert(isinstance(hl, HighLighter))


def test_can_call_highlighter_highlight():
    hl = HighLighter(RankingLexer(), STYLE_MAP)
    hl.highlight("foo")


def test_highlighter_highlight_doesnt_change_input():
    input_text = "make Foo not war"
    input_text_copy = copy(input_text)

    hl = HighLighter(RankingLexer(), STYLE_MAP)
    hl.highlight(input_text)

    assert(input_text == input_text_copy)


def test_highlighter_highlight_correct():
    expected_results = [
        "[49m[1m[36mJessie[39m[22m[49m is [49m[22m[91mnot[39m[22m[49m the [49m[1m[32mbest[39m[22m[49m developer",
        "[49m[1m[36mEvan[39m[22m[49m is [49m[22m[91mnot[39m[22m[49m the [49m[1m[95mworst[39m[22m[49m developer",
        "[49m[1m[36mJohn[39m[22m[49m is [49m[22m[91mnot[39m[22m[49m the [49m[1m[32mbest[39m[22m[49m developer [49m[22m[93mor[39m[22m[49m the [49m[1m[95mworst[39m[22m[49m developer",
        "[49m[1m[36mSarah[39m[22m[49m is a [49m[22m[32mbetter[39m[22m[49m developer than [49m[1m[36mEvan[39m[22m[49m",
        "[49m[1m[36mMatt[39m[22m[49m is [49m[22m[91mnot[39m[22m[49m directly [49m[22m[95mbelow[39m[22m[49m [49m[22m[93mor[39m[22m[49m [49m[22m[32mabove[39m[22m[49m [49m[1m[36mJohn[39m[22m[49m as a developer",
        "[49m[1m[36mJohn[39m[22m[49m is [49m[22m[91mnot[39m[22m[49m directly [49m[22m[95mbelow[39m[22m[49m [49m[22m[93mor[39m[22m[49m [49m[22m[32mabove[39m[22m[49m [49m[1m[36mEvan[39m[22m[49m as a developer",
        ]

    hl = HighLighter(RankingLexer(), STYLE_MAP)

    for i, val in enumerate(programmer_riddle):
        result = hl.highlight(val)
        assert(result == expected_results[i])
