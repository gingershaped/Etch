class Instruction:
    def __init__(self, interpreter):
        self.interpreter = interpreter

class Context():
    def __init__(self, parent):
        self.vars = {}
        self.parent = parent
        self.globals = []
    def getVar(self, name):
        if name in self.vars.keys():
            return self.vars[name]
        elif self.parent:
            return self.parent.getVar(name)
        else:
            raise UnboundLocalError("Invalid variable: " + name)
    def setVar(self, name, value):
        if self.parent:
            if name in self.parent.vars:
                self.parent.setVar(name, value)
            else:
                self.vars[name] = value
        else:
            self.vars[name] = value


class ParameterWrapper():
    def __init__(self, value):
        self.value = value
    def execute(self, context):
        if type(self.value) == Instruction:
            return self.value.execute(context)
        elif type(self.value) == list:
            return [i.execute(context) for i in self.value]
        else:
            return self.value

class PartialWrapper():
    '''functools partial() compatibility replacement'''
    def __init__(self, func, *args):
        self.func = func
        self.args = args
    def execute(self, context):
        return self.func(*[i.execute(context) for i in self.args])