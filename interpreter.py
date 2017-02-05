import random

import AST
from AST import addToClass
from functools import reduce

from svg_writer import SvgWriter as svg

operations = {
    '+': lambda x, y: x + y,
    '-': lambda x, y: x - y,
    '*': lambda x, y: x * y,
    '/': lambda x, y: x / y,
    '%': lambda x, y: x % y,
    '^': lambda x, y: x ** y,
    '==': lambda x,y: x == y,
    '!=': lambda x,y: x != y,
    '<':  lambda x,y: x < y,
    '<=': lambda x,y: x <= y,
    '>':  lambda x,y: x > y,
    '>=': lambda x,y: x >= y,
}
vars = {}


#
# AST
#

@addToClass(AST.ProgramNode)
def execute(self):
    for c in self.children:
        c.execute()


@addToClass(AST.MethodNode)
def execute(self):
    # récupère une méthode de la classe svgWriter qui a le nom self.method
    methodToCall = getattr(svg, self.method)
    if self.children:
        methodToCall(self.children[0].execute())  # children[0] contient le ArgumentNode
    else:
        methodToCall()

@addToClass(AST.FunctionNode)
def execute(self):
    if self.f == "rand":
        if not self.children:
            return random.random()
        else:
            args = self.children[0].execute()
            return random.randrange(*args)


@addToClass(AST.WhileNode)
def execute(self):
    while self.children[0].execute():
        self.children[1].execute()

@addToClass(AST.IfNode)
def execute(self):
    if self.children[0].execute():
        self.children[1].execute()

@addToClass(AST.IfElseNode)
def execute(self):
    if self.children[0].execute():
        self.children[1].execute()
    else:
        self.children[2].execute()


@addToClass(AST.TokenNode)
def execute(self):
    return self.tok


@addToClass(AST.OpNode)
def execute(self):
    args = [c.execute() for c in self.children]
    if len(args) == 1:
        args.insert(0, 0)
    return reduce(operations[self.op], args)


@addToClass(AST.ArgumentNode)
def execute(self):
    # reourne les valeurs des arguments dans une liste
    return [child.execute() for child in self.children]


@addToClass(AST.AssignNode)
def execute(self):
    vars[self.children[0].tok] = self.children[1].execute()


@addToClass(AST.VariableNode)
def execute(self):
    try:
        return vars[self.tok]
    except KeyError:
        print("variable {} undefined !".format(self.tok))


#
# Main
#

if __name__ == "__main__":
    from yacc_parser import parse
    import sys

    try:
        filename = sys.argv[1]
    except:
        filename = "test.txt"

    try:
        prog = open(filename).read()
    except:
        print("Le fichier {} n'a pas pu être lu".format(filename))
        sys.exit()

    ast = parse(prog)
    ast.execute()
    svg.finish()

    with open('output.svg', 'w') as f:
        f.write(svg.svg)
