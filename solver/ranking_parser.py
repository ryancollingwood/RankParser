from ply import yacc

from .ranking_lexer import RankingLexer
from .ranking_problem import RankingProblem

"""
Taking 'inspiration' from https://github.com/kmanley/redisql/blob/master/sqlparser.py
"""


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

    def remove_last_constraint(self):
        if len(self._rp._constraints) > 0:
            del self._rp._constraints[-1]

    def solve(self):
        return self._rp.solve()

    def parse(self, text):
        lexer = RankingLexer().build()
        return self.parser.parse(text, lexer=lexer)

    def parse_statements(self, statements):
        self.build()
        lexer = RankingLexer().build()

        result = ""
        for s in statements:
            result = self.parser.parse(s, lexer=lexer)
        return result[-1][-1]


