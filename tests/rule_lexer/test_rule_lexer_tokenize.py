import pytest
from rule_lexer import RuleLexer
from ply.lex import LexToken
from grammar.consts import *

def test_can_call_rule_lexer_tokenize():
    rl = RuleLexer()
    rl.tokenize(["hello"])


def test_rule_lexer_tokenize_return_empty():
    expected_result = [[]]

    rl = RuleLexer()
    actual_result = rl.tokenize(["hello"])

    assert(actual_result == expected_result)


def test_rule_lexer_tokenize_throws_input_error():
    input_text = "Ryan is not the worst"

    rl = RuleLexer()

    with pytest.raises(TypeError, match=r"Expected List, got .*"):
        rl.tokenize(input_text)


def test_rule_lexer_tokenize_return_tokens_single_statement():
    input_statements = [
        "Ryan is not the worst"
    ]

    rl = RuleLexer()
    actual_result = rl.tokenize(input_statements)
    for t in actual_result[0]:
        assert(isinstance(t, LexToken))


def test_rule_lexer_tokenize_correct_tokens_single_statement():
    input_statements = [
        "Ryan is not the worst"
    ]

    expected_result_types = [
        [PERSON, NOT, WORST],
    ]

    rl = RuleLexer()
    actual_result = rl.tokenize(input_statements)

    assert([x.type for x in actual_result[0]] == expected_result_types[0])

