import ply.lex as lex

reserved_words = (
	'title',
	'desc',
	'pos',
	'move',
	'fill',
	'nofill',
	'stroke',
	'nostroke',
	'rect',
	'line',
	'ellipse',
	'text',
	'while'
)

tokens = (
	'NUMBER',
	'ADD_OP',
	'MULT_OP',
	'STRING',
	'VARIABLE',
) + tuple(w.upper() for w in reserved_words)

literals = '(),='

def t_NUMBER(t):
	r'\d+(\.\d+)?'
	try:
		t.value = float(t.value)    
	except ValueError:
		print ("Line %d: Problem while parsing %s!" % (t.lineno,t.value))
		t.value = 0
	return t
	
def t_ADD_OP(t):
	r'[+-]'
	return t
	
def t_MUL_OP(t):
	r'[*/]'
	return t

def t_VARIABLE(t):
	r'\$[A-Za-z_]\w*'
	return t

def t_STRING(t):
	r'\".*?\"'
	return t
	
def t_RESERVEDWORDS(t):
	r'[A-Za-z_]\w*'
	if t.value in reserved_words:
		t.type = t.value.upper()
		return t
	else:
		print("Erreur lexicale: Le mot {} n'est pas connu".format(t.value))
	
	
def t_newline(t):
	r'\n+'
	t.lexer.lineno += len(t.value)

t_ignore  = ' \t'

def t_error(t):
	print ("Illegal character '%s'" % repr(t.value[0]))
	t.lexer.skip(1)

lex.lex()

if __name__ == "__main__":
	import sys
	prog = open(sys.argv[1]).read()

	lex.input(prog)

	while 1:
		tok = lex.token()
		if not tok: break
		print ("line %d: %s(%s)" % (tok.lineno, tok.type, tok.value))
