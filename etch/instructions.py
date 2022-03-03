class Instruction:
    def __init__(self, interpreter):
        self.interpreter = interpreter
class FunctionCallInstruction(Instruction):
    def __init__(self, interpreter, cls, name, *args):
        self.interpreter = interpreter
        self.cls = cls
        self.name = name
        self.args = args
    def execute(self, context):
        try:
            if self.cls:
                i = context.getClass(self.cls).getFunction(self.name)(self.interpreter, *[i.execute(context) for i in self.args])
            else:
                i = context.getFunction(self.name)(self.interpreter, *[i.execute(context) for i in self.args])
        except KeyError:
            raise ValueError("Undefined function: " + self.name) from None
        return i.execute(context)


class IfInstruction(Instruction):
    def __init__(self, interpreter, elif_, condition, ifTrue, ifFalse):
        self.interpreter = interpreter
        self.condition = condition
        print(condition)
        self.true = ifTrue
        self.false = ifFalse
        if elif_:
            self.elif_ = IfInstruction(interpreter, elif_[1:], interpreter.processInstruction(elif_[0][0]), interpreter.processStatements(elif_[0][1]), None)
        else:
            self.elif_ = None
    
    def execute(self, context):
        if self.condition.execute(context):
            for i in self.true:
                i.execute(context)
            return True
        elif self.elif_:
            if self.elif_.execute(context):
                return True
        if self.false:
            for i in self.false:
                i.execute(context)
            return False

class OutInstruction(Instruction):
    def __init__(self, interpreter, *args):
        self.data = args
    def execute(self, context):
        print(*[i.execute(context) for i in self.data])

class ForeverInstruction(Instruction):
    def __init__(self, interpreter, statements):
        self.statements = statements
    def execute(self, context):
        while True:
            for i in self.statements:
                i.execute(context)
class CountInstruction(Instruction):
    def __init__(self, interpreter, iterations, statements):
        self.iterations = iterations
        self.statements = statements
    def execute(self, context):
        for x in range(self.iterations.execute(context)):
            for i in self.statements:
                i.execute(context)
class WhileInstruction(Instruction):
    def __init__(self, interpreter, condition, statements):
        self.condition = condition
        self.statements = statements
    def execute(self, context):
        while self.condition.execute(context):
            for i in self.statements:
                i.execute(context)

class AssignInstruction(Instruction):
    def __init__(self, interpreter, name, value):
        self.name = name
        self.value = value
    def execute(self, context):
        context.setVar(self.name, self.value.execute(context))
class VariableReadInstruction(Instruction):
    def __init__(self, interpreter, name):
        self.name = name
    def execute(self, context):
        return context.getVar(self.name)
class SomecrementInstruction(Instruction):
    def __init__(self, interpreter, op, name):
        self.op = op
        self.name = name
    def execute(self, context):
        context.setVar(self.name, context.getVar(self.name) + 1)
class InPlaceModifyInstruction(Instruction):
    def __init__(self, interpreter, name, op, expr):
        self.name = name
        self.expr = expr
        self.op = op
    def execute(self, context):
        context.setVar(self.name, self.op(context.getVar(self.name), self.expr.execute(context)))


BUILTINS = {
    "out": OutInstruction
}