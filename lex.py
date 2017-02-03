import ply.lex as lex

methods = (
    'pos',
    'move',
    'clean',
    'size',
    'title',
    'desc',
    'fill',
    'nofill',
    'stroke',
    'nostroke',
    'width',
    'rect',
    'line',
    'ellipse',
    'text',
    'clean'
)

functions = {
    'sin','cos','tan','str','int','rand'
}

tokens = (
    'METHODS',
    'FUNCTIONS',
    'NUMBER',
    'STRING',
    'ADD_OP',
    'MUL_OP',
    'MOD_OP',
    'CONDITION_OP',
    'VARIABLE',
    'WHILE'
)  # + tuple(w.upper() for w in reserved_words)

literals = '(),={}'


def t_NUMBER(t):
    r'\d+(\.\d+)?'
    try:
        t.value = float(t.value)
    except ValueError:
        print("Line %d: Problem while parsing %s!" % (t.lineno, t.value))
        t.value = 0
    return t


def t_ADD_OP(t):
    r'[+-]'
    return t


def t_MUL_OP(t):
    r'[*/]'
    return t

def t_MOD_OP(t):
    r'%'
    return t

def t_CONDITION_OP(t):
    r'==|!=|<=|>=|<|>'
    return t


def t_VARIABLE(t):
    r'\$[A-Za-z_]\w*'
    return t


def t_STRING(t):
    r'\".*?\"'
    return t


def t_WHILE(t):
    r'while'
    return t

def t_COMMENT(t):
    r'\#.*'
    pass


def t_RESERVEDWORDS(t):
    r'[A-Za-z_]\w*'
    if t.value in methods:
        t.type = "METHODS"
        return t
    elif t.value in functions:
        t.type = "FUNCTIONS"
        return t
    print("Erreur lexicale: Le mot {} n'est pas connu".format(t.value))


def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)


t_ignore = ' \t'


def t_error(t):
    print("Illegal character '%s'" % repr(t.value[0]))
    t.lexer.skip(1)


lex.lex()

if __name__ == "__main__":
    import sys

    try:
        filename = sys.argv[1]
    except:
        filename = "test.txt"

    prog = open(filename).read()

    lex.input(prog)

    while 1:
        tok = lex.token()
        if not tok: break
        print("line %d: %s(%s)" % (tok.lineno, tok.type, tok.value))
