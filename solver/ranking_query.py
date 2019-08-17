from ply import lex, yacc
from .ranking_problem import RankingProblem
from typing import List

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

    def test(self):
        self.build()

        while True:
            text = input("RankLexer> ").strip()
            if text.lower() == "quit":
                pass
            self.lexer.input(text)
            while True:
                tok = self.lexer.token()
                if not tok:
                    break
                break
                print(tok)


class RankingParser(object):
    tokens = RankingLexer.tokens

    def __init__(self):
        self._rp = RankingProblem()
        self.parser = None

    # Error rule for syntax errors
    def p_error(self, p):
        if p is None:
            print("Syntax error in input!")
        elif "value" in dir(p):
            print("Syntax error in input!", p.value)
        else:
            print("Syntax error in input!", p)

    def p_statement_list(self, p):
        """
        statement_list : statement
                       | statement_list statement
        """
        if len(p) == 2:
            p[0] = [p[1]]
        else:
            p[0] = p[1] + [p[2]]

    def p_statement(self, p):
        """
        statement : is_before_statement
                  | is_after_statement
                  | not_first_statement
                  | not_last_statement
                  | not_first_or_last_statement
                  | not_directly_above_or_below_statement
        """
        p[0] = p[1]

    def p_is_before_statement(self, p):
        """
        is_before_statement : PERSON BETTER PERSON
        """
        self._rp.add_item(p[1])
        self._rp.add_item(p[3])
        self._rp.is_before(p[1], p[3])
        p[0] = self._rp.solve()

    def p_is_after_statement(self, p):
        """
        is_after_statement : PERSON WORSE PERSON
        """
        self._rp.add_item(p[1])
        self._rp.add_item(p[3])
        self._rp.is_after(p[1], p[3])
        p[0] = self._rp.solve()

    def p_not_first_statement(self, p):
        """
        not_first_statement : PERSON NOT BEST
        """
        self._rp.add_item(p[1])
        self._rp.not_first(p[1])
        p[0] = self._rp.solve()

    def p_not_last_statement(self, p):
        """
        not_last_statement : PERSON NOT WORST
        """
        self._rp.add_item(p[1])
        self._rp.not_last(p[1])
        p[0] = self._rp.solve()

    def p_not_first_or_last_statement(self, p):
        """
        not_first_or_last_statement : PERSON NOT BEST OR WORST
                                    | PERSON NOT WORST OR BEST
        """
        self._rp.add_item(p[1])
        self._rp.not_first(p[1])
        self._rp.not_last(p[1])
        p[0] = self._rp.solve()

    def p_not_directly_above_or_below_statement(self, p):
        """
        not_directly_above_or_below_statement : PERSON NOT DIRECT BETTER OR WORSE PERSON
                                              | PERSON NOT DIRECT WORSE OR BETTER PERSON
        """
        self._rp.add_item(p[1])
        self._rp.add_item(p[7])
        self._rp.not_directly_before_or_after(p[1], p[7])
        p[0] = self._rp.solve()

    def build(self, **kwargs):
        self.parser = yacc.yacc(module=self, **kwargs)
        return self.parser

    def test(self):
        self.build()
        lexer = RankingLexer().build()

        while True:
            text = input("RankParser> ").strip()
            if text.lower() == "quit":
                break

            if text != "":
                if text == "undo":
                    del self._rp._constraints[-1]
                    print(self._rp.solve())
                else:
                    result = self.parser.parse(text, lexer=lexer)
                    print(f"{result}")

    def parse_statements(self, statements):
        self.build()
        lexer = RankingLexer().build()

        result = ""
        for s in statements:
            result = self.parser.parse(s, lexer=lexer)
        return result[-1][-1]


def test_lexer():
    lexer = RankingLexer()
    lexer.test()


def test_parser():
    parser = RankingParser()
    parser.test()


if __name__ == "__main__":
    test_parser()

