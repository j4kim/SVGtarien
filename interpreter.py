import AST
from AST import addToClass
from functools import reduce

svg=""
x=[0,0]
y=[0,0]

def title(args):
	r=args[0].tok
	append('    <title>{}</title>'.format(r[1:-1]))

def desc(args):
	r=args[0].tok
	append('    <desc>{}</desc>'.format(r[1:-1]))

def rect():
    rx = x[-2]
    ry = y[-2]
    w = x[-1] - rx
    h = y[-1] - ry
    append('    <rect x="{}" y="{}" width="{}" height="{}" fill="yellow"/>'.format(rx,ry,w,h))

def ellipse(args):
    r=args[0].tok
    append('    <circle cx="{}" cy="{}" r="{}" stroke="black" stroke-width="3" fill="red" />'.format(x[-1],y[-1],r))

def pos(args):
    global x,y
    x.append(args[0].tok)
    y.append(args[1].tok)

def append(str):
    global svg
    svg += str + '\n'


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
