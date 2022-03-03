from etch.parser.parser import parse
from etch.utils import *
from etch.instructions import *
from operator import *

MATH = {
    "+": add,
    "-": sub,
    "*": mul,
    "/": truediv,
    "//": floordiv,
    "%": mod,
    "^": pow
}
LOGIC = {
    "NOT": not_,
    "<": lt,
    ">": gt,
    "<=": le,
    ">=": ge,
    "==": eq,
    "!=": ne
}

class Interpreter():
    def __init__(self):
        self.context = Context(self, None)
        self.currentContext = self.context
        for b in BUILTINS:
            self.context.functions[b] = BUILTINS[b]

    def processParams(self, params):
        # Helper function for parameters
        return [ParameterWrapper(self.processInstruction(i)) for i in params]
    def processStatements(self, statements):
        return [self.processInstruction(i) for i in statements] if statements != None else None
            
    def processInstruction(self, instruction):
        if instruction == None:
            return None
        try:
            node, params = instruction
        except ValueError:
            print("Parser broke! at instruction:", instruction)
            raise
        if node == "EXPRESSION":
            return self.processExpression(params)
        elif node == "BLOCK":
            return self.processBlock(params)
        elif node == "VALUE":
            if type(params) == list:
                return ParameterWrapper(self.processStatements(params))
            else:
                return ParameterWrapper(params)
        elif node == "ASSIGN":
            return AssignInstruction(self, params[0], self.processInstruction(params[1]))
        elif node == "VARIABLE":
            return VariableReadInstruction(self, params)
        elif node == "SOMECREMENT":
            return SomecrementInstruction(self, *params)

    def processExpression(self, instruction):
        node, params = instruction
        if node == "MATH":
            return PartialWrapper(MATH[params[0]], *self.processStatements(params[1]))
        elif node == "LOGIC":
            return PartialWrapper(LOGIC[params[0]], *self.processStatements(params[1]))
        elif node == "FUNCTION":
            return FunctionCallInstruction(self, params[0], params[1], *self.processParams(params[2]))
            
    def processBlock(self, instruction):
        node, params = instruction
        if node == "IF":
            return IfInstruction(self, params[0], self.processInstruction(params[1]), self.processStatements(params[2]), self.processStatements(params[3]))
        elif node == "FOREVER":
            return ForeverInstruction(self, self.processStatements(params))
        elif node == "COUNT":
            return CountInstruction(self, self.processInstruction(params[1]), self.processStatements(params[0]))
    
        
    def interpret(self, ast):
        print(ast)
        return [self.processInstruction(i) for i in ast]
    def execute(self, instructions):
        for i in instructions:
            i.execute(self.currentContext)
    def run(self, code):
        self.execute(self.interpret(parse(code)))

