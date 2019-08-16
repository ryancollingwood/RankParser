from typing import List
import ply.lex as lex
import grammar


class RuleLexer:
    def __init__(self):
        self._lexer = lex.lex(module=grammar)

    def tokenize(self, statements: List[str]):

        if not(isinstance(statements, List)):
            raise TypeError(f"Expected List, got {type(statements)}")

        result = []

        # Give the lexer some input
        for s in statements:
            output = []
            self._lexer.input(s)

            # Tokenize
            while True:
                tok = self._lexer.token()
                if not tok:
                    break  # No more input
                output.append(tok)

            result.append(output)

        return result
