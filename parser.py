import ply.yacc as yacc

from lex import tokens
import AST

def p_programme_statement(p):
    ''' programme : statement '''
    p[0] = AST.ProgramNode(p[1])

def p_programme_recursive(p):
    ''' programme : statement programme '''
    p[0] = AST.ProgramNode([p[1]]+p[2].children)

def p_statement(p):
    ''' statement : POS
        | MOVE '''
    p[0] = AST.TokenNode(p[1])

def p_expression_num_or_var(p):
    '''statement : NUMBER '''
    p[0] = AST.TokenNode(p[1])

def p_error(p):
    if p:
        print ("Syntax error in line %d" % p.lineno)
        yacc.errok()
    else:
        print ("Sytax error: unexpected end of file!")

'''
precedence = (
    ('left', 'ADD_OP'),
    ('left', 'MUL_OP'),
    ('right', 'UMINUS'),
)
'''

def parse(program):
    return yacc.parse(program)

yacc.yacc(outputdir='generated')

if __name__ == "__main__":
    import sys

    try:
        filename = sys.argv[1]
    except:
        filename = "test.txt"

    prog = open(filename).read()
    result = "coucou"
    result = yacc.parse(prog)

    if result:
        print(result)
    else:
        print("Parsing returned no result!")