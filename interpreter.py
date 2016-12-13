import AST
from AST import addToClass
from functools import reduce

svg=""

def rect():
    return '    <rect width="300" height="100" style="fill:rgb(0,0,255);stroke-width:3;stroke:rgb(0,0,0)" />'

def ellipse():
    return '    <circle cx="50" cy="50" r="40" stroke="black" stroke-width="3" fill="red" />'

def append(str):
    global svg
    svg += str + '\n'


@addToClass(AST.ProgramNode)
def execute(self):
    append('<?xml version="1.0" encoding="utf-8"?>')
    append('<svg xmlns="http://www.w3.org/2000/svg" version="1.1" width="300" height="200">')
    for c in self.children:
        c.execute()
    append('</svg>')


@addToClass(AST.MethodNode)
def execute(self):
    # gloabals() retourne un dictionnaire sur les fonctions globales https://docs.python.org/3/library/functions.html#globals
    append(globals()[self.method]())


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
    ast.execute()

    with open('output.svg', 'w') as f:
        f.write(svg)
