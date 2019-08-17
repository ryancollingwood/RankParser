from solver.ranking_query import RankingLexer


def test_can_create_rule_lexer():
    rl = RankingLexer()
    assert(isinstance(rl, RankingLexer))


