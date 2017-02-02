import random

import AST
from AST import addToClass
from functools import reduce

operations = {
    '+': lambda x, y: x + y,
    '-': lambda x, y: x - y,
    '*': lambda x, y: x * y,
    '/': lambda x, y: x / y,
    '%': lambda x, y: x % y,
}
vars = {}


#
# AST
#

@addToClass(AST.ProgramNode)
def execute(self, writer):
    for c in self.children:
        if isinstance(c, AST.MethodNode) or isinstance(c, AST.WhileNode):
            c.execute(writer)
        else:
            c.execute()


@addToClass(AST.MethodNode)
def execute(self, writer):

    # récupère une méthode de l'objet writer qui a le nom self.method
    methodToCall = getattr(writer, self.method)
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
def execute(self, writer):
    while self.children[0].execute():
        self.children[1].execute(writer)


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
        print("variable %s undefined !" % self.tok)


#
# Main
#

if __name__ == "__main__":
    from svg_parser import parse
    from svg_writer import SvgWriter
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
    writer = SvgWriter()
    ast.execute(writer)
    writer.finish()

    with open('output.svg', 'w') as f:
        f.write(writer.svg)
