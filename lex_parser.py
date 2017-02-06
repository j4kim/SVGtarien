import ply.lex as lex

methods = (
    'pos', 'move', 'clean',
    'size', 'title', 'desc',
    'fill', 'nofill', 'stroke', 'nostroke', 'width', 'font',
    'rotate', 'scale', 'notransform',
    'rect', 'line', 'ellipse', 'text'
)

functions = {
    'sin','cos','tan',
    's','i',
    'rand'
}

structures = {
    'while', 'if', 'else'
}

tokens = (
    'METHODS', 'FUNCTIONS', 'ROUTINE',
    'NUMBER', 'STRING', 'VARIABLE',
    'ADD_OP', 'MUL_OP', 'MOD_OP', 'CONDITION_OP', 'POW_OP'
) + tuple(map(lambda s:s.upper(), structures))

literals = '(),={}'

t_ADD_OP = r'[+-]'
t_POW_OP = r'\^'
t_MUL_OP = r'[*/]'
t_MOD_OP = r'%'
t_CONDITION_OP = r'==|!=|<=|>=|<|>'
t_VARIABLE = r'\$[A-Za-z_]\w*'

def t_NUMBER(t):
    r'\d+(\.\d+)?'
    try:
        t.value = float(t.value)
    except ValueError:
        print("Line %d: Problem while parsing %s!" % (t.lineno, t.value))
        t.value = 0
    return t

def t_STRING(t):
    r'\".*?\"'
    t.value = t.value[1:-1] # [1:-1] enlève les guillemets de la string
    return t

def t_COMMENT(t):
    r'[#].*'
    pass

def t_RESERVEDWORDS(t):
    r'[A-Za-z_]\w*'
    if t.value in methods:
        t.type = "METHODS"
    elif t.value in functions:
        t.type = "FUNCTIONS"
    elif t.value in structures:
        t.type = t.value.upper()
    else:
        t.type = "ROUTINE"
    return t

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
