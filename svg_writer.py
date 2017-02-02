from options import Options


class SvgWriter:
    def __init__(self):
        self.svg = ""
        self.x = []
        self.y = []
        self.options = Options()
        self.w = self.h = 0
        self.sizeFixed = False

    def title(self, args):
        self.write('    <title>{}</title>'.format(args[0]))

    def desc(self, args):
        self.write('    <desc>{}</desc>'.format(args[0]))

    def text(self, args):
        self.write('    <text x="{}" y="{}" {}>{}</text>'.format(self.x[-1], self.y[-1], self.options, args[0]))

    def rect(self,args=None):
        if not args:
            x1, x2 = self.x[-2], self.x[-1]
            y1, y2 = self.y[-2], self.y[-1]
            # on s'assure d'avoir des valeurs positives pour w et h
            if x2 < x1: x1, x2 = x2, x1  # swap x1 et x2
            if y2 < y1: y1, y2 = y2, y1  # swap y1 et y2
            w, h = x2 - x1, y2 - y1
        else:
            x1 = self.x[-1]
            y1 = self.y[-1]
            w = args[0]
            try: h = args[1]
            except: h=w

        self.write('    <rect x="{}" y="{}" width="{}" height="{}" {}/>'.format(x1, y1, w, h, self.options))

    def ellipse(self, args):
        r = args[0]
        self.write('    <circle cx="{}" cy="{}" r="{}" {}/>'.format(self.x[-1], self.y[-1], r, self.options))

    def line(self, *args):
        list_point = ""
        x = self.x
        y = self.y
        if args:  # If args is not empty.
            if args[0][0] > 1:
                for i in range(int(args[0][0])):
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
        if not self.sizeFixed:
            if x > self.w: self.w = x
            if y > self.h: self.h = y

    def pos(self, args):
        self.updatePos(args[0], args[1])

    def move(self, args):
        self.updatePos(self.x[-1] + args[0], self.y[-1] + args[1])

    def clean(self):
        self.x = []
        self.y = []

    def size(self, args):
        self.w = args[0]
        self.h = args[1]
        self.sizeFixed = True

    #
    # Change color/stroke options
    #

    def fill(self, args):
        if len(args) > 2:
            r = int(args[0])
            g = int(args[1])
            b = int(args[2])
            try: a = args[3]
            except: a = 1
            self.options.add("fill", "rgba({},{},{},{})".format(r,g,b,a))
        else:
            self.options.add("fill", args[0])

    def stroke(self, args):
        # todo: dry
        if len(args) > 2:
            r = int(args[0])
            g = int(args[1])
            b = int(args[2])
            try: a = args[3]
            except: a = 1
            self.options.add("stroke", "rgba({},{},{},{})".format(r,g,b,a))
        else:
            self.options.add("stroke", args[0])

    def width(self, arg):
        self.options.add("stroke-width", arg[0])

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
                   '<svg xmlns="http://www.w3.org/2000/svg" version="1.1" width="{}" height="{}">\n' \
                       .format(self.w, self.h) + self.svg
        self.write('</svg>')
