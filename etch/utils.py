from etch.instructions import Instruction

class Context():
    def __init__(self, parent):
        self.vars = {}
        self.functions = {}
        self.classes = {}
        self.parent = parent
        self.globals = []
    def getFunction(self, name):
        if name in self.functions.keys():
            return self.functions[name]
        else:
            if self.parent:
                return self.parent.getFunction(name)
            else:
                raise KeyError
    def getClass(self, name):
        if name in self.classes.keys():
            return self.classes[name]
        else:
            if self.parent:
                return self.parent.getClass(name)
            else:
                raise KeyError
    def getVar(self, name):
        if name in self.vars.keys():
            return self.vars[name]
        elif name in self.globals:
            if self.parent:
                return self.parent.getVar(name)
            else:
                raise UnboundLocalError("Invalid variable: " + name)
    def setVar(self, name, value):
        if name in self.globals and self.parent:
            self.parent.setVar(name, value)
        else:
            self.vars[name] = value


class ParameterWrapper():
    def __init__(self, value):
        self.value = value
    def execute(self, context):
        if type(self.value) == Instruction:
            return self.value.execute(context)
        else:
            return self.value

class PartialWrapper():
    '''functools partial() compatibility replacement'''
    def __init__(self, func, *args):
        self.func = func
        self.args = args
    def execute(self, context):
        return self.func(*[i.execute(context) for i in self.args])