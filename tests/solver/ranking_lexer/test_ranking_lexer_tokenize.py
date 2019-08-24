import pytest
from solver import RankingLexer
from ply.lex import LexToken


def test_can_call_rule_lexer_tokenize():
    rl = RankingLexer()
    rl.tokenize("hello")


def test_rule_lexer_tokenize_return_empty():
    expected_result = []

    rl = RankingLexer()
    actual_result = rl.tokenize("hello")

    assert(actual_result == expected_result)


def test_rule_lexer_tokenize_throws_input_error():
    input_text = ["Ryan is not the worst"]

    rl = RankingLexer()

    with pytest.raises(TypeError, match=r"Expected str, got .*"):
        rl.tokenize(input_text)


def test_rule_lexer_tokenize_return_tokens_single_statement():
    input_statement = "Ryan is not the worst"

    rl = RankingLexer()
    actual_result = rl.tokenize(input_statement)
    for t in actual_result:
        assert(isinstance(t, LexToken))


def test_rule_lexer_tokenize_correct_tokens_single_statement():
    input_statement = "Ryan is not the worst"

    expected_result_types = [
        "PERSON", "NOT", "WORST"
    ]

    rl = RankingLexer()
    actual_result = rl.tokenize(input_statement)

    assert([x.type for x in actual_result] == expected_result_types)

