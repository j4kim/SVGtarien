from options import Options

class SvgWriter:

    def __init__(self):
        self.svg = ""
        self.x = []
        self.y = []
        self.options = Options()
        self.w = self.h = 0

    def title(self, args):
        self.write('    <title>{}</title>'.format(args[0].tok))

    def desc(self, args):
        self.write('    <desc>{}</desc>'.format(args[0].tok))

    def text(self, args):
        self.write('    <text x="{}" y="{}" {}>{}</text>'.format(self.x[-1], self.y[-1], self.options, args[0].tok))

    def rect(self):
        x1, x2 = self.x[-2], self.x[-1]
        y1, y2 = self.y[-2], self.y[-1]
        # on s'assure d'avoir des valeurs positives pour w et h
        if x2<x1 : x1,x2 = x2,x1 # swap x1 et x2
        if y2<y1 : y1,y2 = y2,y1 # swap y1 et y2
        w, h = x2-x1, y2-y1

        self.write('    <rect x="{}" y="{}" width="{}" height="{}" {}/>'.format(x1, y1, w, h, self.options))

    def ellipse(self, args):
        r = args[0].tok
        self.write('    <circle cx="{}" cy="{}" r="{}" {}/>'.format(self.x[-1], self.y[-1], r, self.options))

    def line(self, *args):
        list_point = ""
        x = self.x
        y = self.y
        if args:  # If args is not empty.
            if args[0][0].tok > 1:
                for i in range(int(args[0][0].tok)):
                    list_point += (str(x[-i - 1]) + "," + str(y[-i - 1]) + " ")
            else:
                list_point += (str(x[-2]) + "," + str(y[-2]) + " " + str(x[-1]) + "," + str(y[-1]))

        else:
            for i in range(len(x)):
                list_point += (str(x[-i - 1]) + "," + str(y[-i - 1]) + " ")
        self.write('    <polyline points="{}" {}/>'.format(list_point, self.options))


    #
    # move cursor
    #

    def updatePos(self, x, y):
        self.x.append(x)
        self.y.append(y)
        if x > self.w: self.w = x
        if y > self.h: self.h = y

    def pos(self, args):
        self.updatePos(args[0].tok, args[1].tok)

    def move(self, args):
        self.updatePos(self.x[-1] + args[0].tok, self.y[-1] + args[1].tok)

    #
    # Change color/stroke options
    #

    def fill(self, arg):
        self.options.add("fill", arg[0].tok)

    def stroke(self, arg):
        self.options.add("stroke", arg[0].tok)

    def width(self, arg):
        self.options.add("stroke-width", arg[0].tok)

    def nofill(self):
        self.options.remove("fill")

    def nostroke(self):
        self.options.remove("stroke")
        self.options.remove("stroke-width")

    #
    # Write a new line in the svg
    #

    def write(self, str):
        self.svg += str + '\n'

    #
    # init
    #

    def finish(self):
        self.svg = '<?xml version="1.0" encoding="utf-8"?>\n' \
                   '<svg xmlns="http://www.w3.org/2000/svg" version="1.1" width="{}" height="{}">\n'\
                       .format(self.w, self.h) + self.svg
        self.write('</svg>')