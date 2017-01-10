class Node:
    count = 0
    type = 'Node (unspecified)'
    shape = 'ellipse'
    def __init__(self,children=None):
        self.ID = str(Node.count)
        Node.count+=1
        if not children: self.children = []
        elif hasattr(children,'__len__'):
            self.children = children
        else:
            self.children = [children]
        self.next = []

    def addNext(self,next):
        self.next.append(next)

    def asciitree(self, prefix=''):
        result = "%s%s\n" % (prefix, repr(self))
        prefix += '|  '
        for c in self.children:
            if not isinstance(c,Node):
                result += "%s*** Error: Child of type %r: %r\n" % (prefix,type(c),c)
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
        return repr(self.tok)
    
class OpNode(Node):
    def __init__(self, op, children):
        Node.__init__(self,children)
        self.op = op
        try:
            self.nbargs = len(children)
        except AttributeError:
            self.nbargs = 1
        
    def __repr__(self):
        return "%s (%s)" % (self.op, self.nbargs)
    
class AssignNode(Node):
    type = '='
    
class PrintNode(Node):
    type = 'print'

class MethodNode(Node):
    type = 'method'

    def __init__(self, method, children=[]):
        Node.__init__(self, children)
        self.method = method

    def __repr__(self):
        return "method "+ self.method

class ArgumentNode(Node):
    type='arguments'

class WhileNode(Node):
    type = 'while'
    
class EntryNode(Node):
    type = 'ENTRY'
    def __init__(self):
        Node.__init__(self, None)

class VariableNode(TokenNode):
	type = 'variable'
    
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
        setattr(cls,func.__name__,func)
        return func
    return decorator