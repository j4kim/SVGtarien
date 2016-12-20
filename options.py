class Options:

    def __init__(self):
        self.options = {}

    def add(self, key, value):
        self.options[key] = value

    def remove(self, key):
        if key in self.options:
            del self.options[key]

    def __repr__(self):
        str=''
        for key, value in self.options.items():
            str+='{}="{}" '.format(key,value)
        return str