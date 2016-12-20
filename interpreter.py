import AST
from AST import addToClass
from functools import reduce
from options import Options

svg=""
x=[0,0]
y=[0,0]
options = Options()

def title(args):
	append('    <title>{}</title>'.format(args[0].tok))

def desc(args):
	append('    <desc>{}</desc>'.format(args[0].tok))

def rect():
    rx = x[-2]
    ry = y[-2]
    w = x[-1] - rx
    h = y[-1] - ry
    append('    <rect x="{}" y="{}" width="{}" height="{}" {}/>'.format(rx,ry,w,h, options))

def ellipse(args):
    r=args[0].tok
    append('    <circle cx="{}" cy="{}" r="{}" {}/>'.format(x[-1],y[-1],r, options))

def pos(args):
    x.append(args[0].tok)
    y.append(args[1].tok)

def move(args):
	x.append(x[-1]+args[0].tok)
	y.append(y[-1]+args[1].tok)


def append(str):
    global svg, options, x, y
    svg += str + '\n'

def fill(arg):
    options.add("fill", arg[0].tok)

def stroke(arg):
    options.add("stroke", arg[0].tok)


@addToClass(AST.ProgramNode)
def execute(self):
    append('<?xml version="1.0" encoding="utf-8"?>')
    append('<svg xmlns="http://www.w3.org/2000/svg" version="1.1" width="800" height="800">')
    for c in self.children:
        c.execute()
    append('</svg>')


@addToClass(AST.MethodNode)
def execute(self):
    # gloabals() retourne un dictionnaire sur les fonctions globales https://docs.python.org/3/library/functions.html#globals
    if self.children:
        globals()[self.method](self.children[0].children) # children[0] contient le ArgumentNode
    else:
        globals()[self.method]()


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
