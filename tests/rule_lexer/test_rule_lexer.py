from rule_lexer import RuleLexer


def test_can_create_rule_lexer():
    rl = RuleLexer()
    assert(isinstance(rl, RuleLexer))


