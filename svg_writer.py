from options import Options

class SvgWriter:

    svg = ""
    x = []
    y = []
    options = Options()
    font_opt = Options()
    w = h = 0
    sizeFixed = False


    @classmethod
    def title(cls, args):
        cls.write('    <title>{}</title>'.format(args[0]))


    @classmethod
    def desc(cls, args):
        cls.write('    <desc>{}</desc>'.format(args[0]))


    @classmethod
    def text(cls, args):
        opt = cls.options.union(cls.font_opt)
        cls.write('    <text x="{}" y="{}" {}>{}</text>'.format(cls.x[-1], cls.y[-1], opt, args[0]))


    @classmethod
    def rect(cls,args=None):
        if not args:
            x1, x2 = cls.x[-2], cls.x[-1]
            y1, y2 = cls.y[-2], cls.y[-1]
            # on s'assure d'avoir des valeurs positives pour w et h
            if x2 < x1: x1, x2 = x2, x1  # swap x1 et x2
            if y2 < y1: y1, y2 = y2, y1  # swap y1 et y2
            w, h = x2 - x1, y2 - y1
        else:
            x1 = cls.x[-1]
            y1 = cls.y[-1]
            w = args[0]
            try: h = args[1]
            except: h=w

        cls.write('    <rect x="{}" y="{}" width="{}" height="{}" {}/>'.format(x1, y1, w, h, cls.options))


    @classmethod
    def ellipse(cls, args):
        rx = args[0]
        try: ry = args[1]
        except: ry=rx
        cls.write('    <ellipse cx="{}" cy="{}" rx="{}" ry="{}" {}/>'.format(cls.x[-1], cls.y[-1], rx, ry, cls.options))


    @classmethod
    def line(cls, args=None):
        list_point = ""
        x, y = cls.x, cls.y
        if args:
            for i in range(int(args[0])):
                list_point += "{},{} ".format(x[-i -1], y[-i -1])
        else:
            for x,y in zip(cls.x, cls.y):
                list_point += "{},{} ".format(x,y)
        cls.write('    <polyline points="{}" {}/>'.format(list_point, cls.options))


    @classmethod
    def bezier(cls, args=None):
        x, y = cls.x, cls.y

        try: closepath = args[0]
        except:closepath = False

        try:
            cls.write('    <path d="M {},{} Q {},{} {},{} {}" {} />'.format(
                x[-3],y[-3], x[-2],y[-2], x[-1],y[-1],
                'Z' if closepath else '',
                cls.options
            ))
        except:
            print("Vous devez définir trois points avant d'appeler la méthode bezier")

    @classmethod
    def path(cls, args):
        # cls.translate([cls.x[-1], cls.y[-1]])
        cls.write('    <path d="{2}" {3} />'.format(
            cls.x[-1], cls.y[-1],
            args[0],
            cls.options
        ))

    #
    # move cursor
    #

    @classmethod
    def updatePos(cls, x, y):
        cls.x.append(x)
        cls.y.append(y)
        if not cls.sizeFixed:
            if x > cls.w: cls.w = x
            if y > cls.h: cls.h = y


    @classmethod
    def pos(cls, args):
        cls.updatePos(args[0], args[1])


    @classmethod
    def move(cls, args):
        cls.updatePos(cls.x[-1] + args[0], cls.y[-1] + args[1])


    @classmethod
    def clean(cls):
        cls.x = []
        cls.y = []


    @classmethod
    def size(cls, args):
        cls.w = args[0]
        cls.h = args[1]
        cls.sizeFixed = True

    #
    # Change style options
    #

    @classmethod
    def rgba(cls, attr, args):
        if len(args) > 2:
            r = int(args[0])
            g = int(args[1])
            b = int(args[2])
            try: a = args[3]
            except: a = 1
            cls.options.add(attr, "rgba({},{},{},{})".format(r,g,b,a))
        else:
            cls.options.add(attr, args[0])


    @classmethod
    def fill(cls, args):
        cls.rgba("fill", args)


    @classmethod
    def stroke(cls, args):
        cls.rgba("stroke", args)


    @classmethod
    def nofill(cls):
        cls.options.remove("fill")


    @classmethod
    def nostroke(cls):
        cls.options.remove("stroke")
        cls.options.remove("stroke-width")


    @classmethod
    def width(cls, arg):
        cls.options.add("stroke-width", arg[0])


    #
    # Transform options
    #

    @classmethod
    def rotate(cls, args):
        try:
            cx = args[1]
            cy = args[2]
        except:
            cx = cls.x[-1]
            cy = cls.y[-1]
        cls.options.append("transform", "rotate({} {} {})".format(args[0], cx, cy))

    @classmethod
    def scale(cls, args):
        sx = args[0]
        try: sy= args[1]
        except: sy= sx
        cls.options.append("transform", "scale({} {})".format(sx, sy))


    @classmethod
    def translate(cls, args):
        dx = args[0]
        try: dy= args[1]
        except: dy= 0
        cls.options.append("transform", "translate({} {})".format(dx, dy))


    @classmethod
    def notransform(cls):
        cls.options.remove("transform")

    #
    # Change font options
    #

    @classmethod
    def font(cls, args):
        cls.font_opt.add("font-size",args[0])
        if len(args) > 1:
            cls.font_opt.add("font-family",args[1])


    #
    # Write a new line in the svg
    #

    @classmethod
    def write(cls, str):
        cls.svg += str + '\n'

    #
    # init
    #

    @classmethod
    def finish(cls):
        cls.svg = '<?xml version="1.0" encoding="utf-8"?>\n' \
                   '<svg xmlns="http://www.w3.org/2000/svg" version="1.1" width="{}" height="{}">\n' \
                       .format(cls.w, cls.h) + cls.svg
        cls.write('</svg>')
