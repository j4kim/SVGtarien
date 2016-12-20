import AST
from AST import addToClass
from functools import reduce
from options import Options

svg=""
x=[]
y=[]
options = Options()
w=h=0

def title(args):
	write('    <title>{}</title>'.format(args[0].tok))

def desc(args):
	write('    <desc>{}</desc>'.format(args[0].tok))

def rect():
    rx = x[-2]
    ry = y[-2]
    w = x[-1] - rx
    h = y[-1] - ry
    write('    <rect x="{}" y="{}" width="{}" height="{}" {}/>'.format(rx, ry, w, h, options))

def ellipse(args):
    r=args[0].tok
    write('    <circle cx="{}" cy="{}" r="{}" {}/>'.format(x[-1], y[-1], r, options))

#
# move cursor
#

def updatePos(nx, ny):
    global w, h
    x.append(nx)
    y.append(ny)
    if nx > w : w = nx
    if nx > h : h = nx

def pos(args):
    updatePos(args[0].tok, args[1].tok)

def move(args):
    updatePos(x[-1]+args[0].tok, y[-1]+args[1].tok)

#
# Change color/stroke options
#

def fill(arg):
    options.add("fill", arg[0].tok)

def stroke(arg):
    options.add("stroke", arg[0].tok)

def width(arg):
    options.add("stroke-width", arg[0].tok)

def nofill():
    options.remove("fill")

def nostroke():
    options.remove("stroke")
    options.remove("stroke-width")

#
# Write a new line in svg
#

def write(str):
    global svg, x, y, options
    svg += str + '\n'

#
# AST
#

@addToClass(AST.ProgramNode)
def execute(self):
    write('<?xml version="1.0" encoding="utf-8"?>')
    write('<svg xmlns="http://www.w3.org/2000/svg" version="1.1" width="800" height="800">')
    for c in self.children:
        c.execute()
    write('</svg>')


@addToClass(AST.MethodNode)
def execute(self):
    if self.children:
        # gloabals() retourne un dictionnaire sur les fonctions globales https://docs.python.org/3/library/functions.html#globals
        globals()[self.method](self.children[0].children) # children[0] contient le ArgumentNode
    else:
        globals()[self.method]()

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
    ast.execute()

    with open('output.svg', 'w') as f:
        f.write(svg)
