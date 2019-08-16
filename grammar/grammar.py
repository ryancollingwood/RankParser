
# using consts here causes the lexer to fail to build :/
tokens = (
    'WHITESPACE',
    'THE',
    'A',
    'AS',
    'AN',
    'IS',
    'NOT',
    'OR',
    'BEST',
    'WORST',
    'BETTER',
    'WORSE',
    'DIRECT',
    'OBJECT',
    'PERSON',
)

# Regular expression rules for simple tokens
t_ignore_WHITESPACE = r'\s{1,}'

t_ignore_THE = r'the'
t_ignore_A = r'a'
t_ignore_AN = r'an'
t_ignore_AS = r'as'
t_ignore_IS = r'is'

t_NOT = r'not'
t_OR = r'or'
t_BEST = r'best'
t_WORST = r'worst'
t_BETTER = r'(better|above|before)'
t_WORSE = r'(worse|below|after)'
t_DIRECT = r'direct(ly)?'

not_objects = "|".join([
    t_ignore_THE, t_ignore_IS, t_NOT,
    t_ignore_A, t_ignore_AN, t_ignore_AS,
    t_BEST, t_WORST, t_BETTER, t_WORSE,
    t_DIRECT,
])
t_ignore_OBJECT = r'(?!' + not_objects + ')[a-z]{3,}'

t_PERSON = r'[A-Z]{1}[a-z]{1,}'


# Error handling rule
def t_error(t):
    print("Illegal character '%s'" % t.value[0])
    t.lexer.skip(1)


# Tracking line numbers
def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)
