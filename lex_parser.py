import ply.lex as lex

# les méthodes modifient le fichier SVG
methods = (
    'pos', 'move', 'clean',  # modification de l'historique de position
    'size', 'title', 'desc', # modification d'attributs de la racine de l'arbre SVG
    'fill', 'nofill', 'stroke', 'nostroke', 'width', 'font', # modif les attributs de dessin
    'rotate', 'scale', 'translate', 'notransform', # modif de l'attribut transform
    'rect', 'line', 'ellipse', 'text', 'bezier', 'path' # dessin d'un nouvel élément
)

# les fonctions retournent des valeurs (sauf debug) elles n'affectent pas le svg
functions = {
    'sin','cos','tan', # fonctions trigonométriques
    's','i',           # foncitons de conversions
    'rand',            # génération de nombres pseudo-aléatoires
    'debug'            # print des valeurs dans la console
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
        print("Line {}: Problem while parsing {}!".format(t.lineno, t.value))
        t.value = 0
    return t


def t_STRING(t):
    r'\".*?\"'
    t.value = t.value[1:-1] # [1:-1] enlève les guillemets de la string
    return t


def t_COMMENT(t):
    r'[#].*'
    pass # on ne fait rien des commentaires, ils sont mis à la poubelle


def t_RESERVEDWORDS(t):
    r'[A-Za-z_]\w*'
    if t.value in methods:
        t.type = "METHODS"
    elif t.value in functions:
        t.type = "FUNCTIONS"
    elif t.value in structures:
        t.type = t.value.upper()
    else:
        t.type = "ROUTINE" # si le mot n'est pas connu, on considère que c'est une routine
    return t


def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)


t_ignore = ' \t'


def t_error(t):
    print("Illegal character '{}'".format(repr(t.value[0])))
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
        print("line {}: {}({})".format(tok.lineno, tok.type, tok.value))
