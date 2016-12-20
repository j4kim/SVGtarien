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
    ''' statement : method '''
    p[0] = p[1]

def p_method_arg(p):
    ''' method : methodName '(' arguments  ')' '''
    p[0] = AST.MethodNode(p[1], [p[3]])

def p_method(p):
    ''' method : methodName '(' ')' '''
    p[0] = AST.MethodNode(p[1])

def p_arguments(p):
    ''' arguments : expression '''
    p[0] = AST.ArgumentNode(p[1])

def p_arguments_list(p):
    ''' arguments : expression ',' expression '''
    p[0] = AST.ArgumentNode([p[1],p[3]])

def p_methodName(p):
    ''' methodName : RESERVEDWORDS'''
    p[0] = p[1]

def p_expression(p):
    '''expression : NUMBER'''
    p[0] = AST.TokenNode(p[1])
	
def p_expression_string(p):
    '''expression : STRING '''
    p[0] = AST.TokenNode(p[1][1:-1]) # [1:-1] enlève les guillemets de la string

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
    result = yacc.parse(prog)

    if result:
        print(result)
    else:
        print("Parsing returned no result!")