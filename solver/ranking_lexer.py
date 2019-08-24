from typing import List

from ply import lex

"""
Taking 'inspiration' from https://github.com/kmanley/redisql/blob/master/sqlparser.py
"""


class RankingLexer(object):

    # using consts here causes the lexer to fail to build :/
    tokens = (
        'NOISE',
        'NOT',
        'OR',
        'BEST',
        'WORST',
        'BETTER',
        'WORSE',
        'DIRECT',
        'PERSON',
    )

    # ignore whitespace and tabs
    t_ignore = ' \t'

    # Regular expression rules for simple tokens
    t_NOT = r'not'
    t_OR = r'or'
    t_BEST = r'(best|first)'
    t_WORST = r'(worst|last)'
    t_BETTER = r'(better|above|before)'
    t_WORSE = r'(worse|below|after)'
    t_DIRECT = r'direct(ly)?'

    t_PERSON = r'[A-Z]{1}[a-z]{1,}'

    # construct a lookahead regex to ignore everything that isn't
    # one of the specified tokens
    ignore_regexes = [f"(?!{x})" for x in [
        t_NOT, t_OR, t_BEST, t_WORST, t_BETTER, t_WORSE, t_DIRECT, t_PERSON
    ]]

    t_ignore_NOISE = r'' + "".join(ignore_regexes) + "[A-Za-z\t]{1,}"

    def __init__(self):
        self.lexer = None

    # Define a rule so we can track line numbers
    def t_newline(self, t):
        r'\n+'
        t.lexer.lineno += len(t.value)

    def t_error(self, t):
        raise TypeError("Unknown text '%s'" % (t.value,))

    def build(self, **kwargs):
        self.lexer = lex.lex(module=self, **kwargs)
        return self.lexer

    def tokenize(self, statement: str):

        if not isinstance(statement, str):
            raise TypeError(f"Expected str, got {type(statement)}")

        self.build()

        result = []
        self.lexer.input(statement)
        while True:
            tok = self.lexer.token()
            if not tok:
                break
            result.append(tok)
        return result

    def lex_statements(self, statements: List[str]):
        self.build()

        for s in statements:
            print(s)
            self.lexer.input(s)
            while True:
                tok = self.lexer.token()
                if not tok:
                    break
                print(tok)
            print()