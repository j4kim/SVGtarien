class Options:

    def __init__(self):
        self.options = {}

    def add(self, key, value):
        self.options[key] = value

    def remove(self, key):
        if key in self.options:
            del self.options[key]

    def union(self, other):
        new = Options()
        new.options = dict(self.options, **other.options)
        return new

    def __repr__(self):
        str=''
        for key, value in self.options.items():
            str+='{}="{}" '.format(key,value)
        return str