class Node:
    type = 'Node (unspecified)'

    def __init__(self, children=None):
        if not children:
            self.children = []
        elif isinstance(children, list):
            self.children = children
        else:
            self.children = [children]

    def asciitree(self, prefix=''):
        result = "{}{}\n".format(prefix, repr(self))
        prefix += '|  '
        for c in self.children:
            if not isinstance(c, Node):
                result += "{}*** Error: Child of type {}: {}\n".format(prefix, type(c), c)
                continue
            result += c.asciitree(prefix)
        return result

    def __str__(self):
        return self.asciitree()

    def __repr__(self):
        return self.type


class ProgramNode(Node):
    type = 'Program'


class TokenNode(Node):
    type = 'token'

    def __init__(self, tok):
        Node.__init__(self)
        self.tok = tok

    def __repr__(self):
        # return repr(self.tok)
        return "{} ({})".format(self.tok, self.type)


class VariableNode(Node):
    type = 'variable'

    def __init__(self, name):
        Node.__init__(self)
        self.name = name


class CallRoutineNode(VariableNode):
    type = 'routine'


class OpNode(Node):
    def __init__(self, op, children):
        Node.__init__(self, children)
        self.op = op
        try:
            self.nbargs = len(children)
        except AttributeError:
            self.nbargs = 1

    def __repr__(self):
        return "%s (%s)" % (self.op, self.nbargs)


class AssignNode(Node):
    type = '='


class AssignRoutineNode(AssignNode):
    pass


class MethodNode(Node):
    type = 'method'

    def __init__(self, method, children=[]):
        Node.__init__(self, children)
        self.method = method

    def __repr__(self):
        return "method " + self.method


class FunctionNode(Node):
    type = 'function'

    def __init__(self, f, children=[]):
        Node.__init__(self, children)
        self.f = f

    def __repr__(self):
        return "function " + self.f


class ArgumentNode(Node):
    type = 'arguments'


class WhileNode(Node):
    type = 'while'


class IfNode(Node):
    type = 'if'


class IfElseNode(Node):
    type = 'ifelse'


def addToClass(cls):
    ''' Décorateur permettant d'ajouter la fonction décorée en tant que méthode
    à une classe.
    
    Permet d'implémenter une forme élémentaire de programmation orientée
    aspects en regroupant les méthodes de différentes classes implémentant
    une même fonctionnalité en un seul endroit.
    
    Attention, après utilisation de ce décorateur, la fonction décorée reste dans
    le namespace courant. Si cela dérange, on peut utiliser del pour la détruire.
    Je ne sais pas s'il existe un moyen d'éviter ce phénomène.
    '''

    def decorator(func):
        setattr(cls, func.__name__, func)
        return func

    return decorator
