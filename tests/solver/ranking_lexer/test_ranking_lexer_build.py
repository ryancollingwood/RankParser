from ply.lex import Lexer
from solver import RankingLexer


def test_can_call_ranking_lexer_build():
    rl = RankingLexer()
    rl.build()


def test_ranking_lexer_build_returns_lex():
    rl = RankingLexer()
    build_result = rl.build()
    assert(isinstance(build_result, Lexer))
