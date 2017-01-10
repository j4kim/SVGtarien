import AST
from AST import addToClass
from svg_writer import SvgWriter


#
# AST
#

@addToClass(AST.ProgramNode)
def execute(self, writer):
    for c in self.children:
        c.execute(writer)
    writer.finish()


@addToClass(AST.MethodNode)
def execute(self, writer):
    methodToCall = getattr(writer, self.method)
    if self.children:
        # gloabals() retourne un dictionnaire sur les fonctions globales https://docs.python.org/3/library/functions.html#globals
        methodToCall(self.children[0].children) # children[0] contient le ArgumentNode
    else:
        methodToCall()

@addToClass(AST.AssignNode)
def execute(self):
    vars[self.children[0].tok] = self.children[1].execute()		

@addToClass(AST.TokenNode)
def execute(self):
    if isinstance(self.tok, str):
        try:
            return vars[self.tok]
        except KeyError:
            print ("*** Error: variable %s undefined!" % self.tok)
    return self.tok

#
# Main
#

if __name__ == "__main__":
    from svg_parser import parse
    import sys

    try:
        filename = sys.argv[1]
    except:
        filename = "test.txt"

    try:
        prog = open(filename).read()
    except:
        print("yolo")
        sys.exit()

    ast = parse(prog)
    writer = SvgWriter()
    ast.execute(writer)

    with open('output.svg', 'w') as f:
        f.write(writer.svg)
