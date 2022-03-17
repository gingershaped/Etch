from etch.parser.parser import EtchParser
from etch.parser.lexer import EtchLexer
from etch.utils import *
from etch.instructions import *
from etch.instructions.operators import *
import etch.mixins
from operator import *
import importlib

__version__ = "0.2.3"
__doc__ = '''Etch, an easy-to-use high-level interpreted language based off of Python.'''

MATH = {
    "+": e_add,
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
    "!=": ne,
    "<>": lambda x, y: 1 if x > y else -1 if x < y else 0
}

class Interpreter():
    def __init__(self, debug = False):
        self.debug = debug
        PARSER_DEBUG = debug
        self.__context__ = Context(None)
        self.lexer = EtchLexer()
        self.parser = EtchParser()
        
        for b in BUILTINS:
            self.__context__.vars[b] = BUILTINS[b]
    
        self.loadModule("etch.stdlib")
        
    def loadModule(self, path):
        m = importlib.import_module(path)
        m.setup(self)

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
        elif node == "IN_PLACE":
            return InPlaceModifyInstruction(self, params[0], MATH[params[1][0]], self.processInstruction(params[2]))
        elif node == "SWAP":
            return SwapInstruction(self, params[0], params[1])
        elif node == "FUNCTION":
            return FunctionDefinitionInstruction(self, params[0], params[1], self.processStatements(params[2]))
        elif node == "RETURN":
            return ReturnInstruction(self, self.processInstruction(params))

    def processExpression(self, instruction):
        node, params = instruction
        if node == "MATH":
            return PartialWrapper(MATH[params[0]], *self.processStatements(params[1]))
        elif node == "LOGIC":
            return PartialWrapper(LOGIC[params[0]], *self.processStatements(params[1]))
        elif node == "FUNCTION":
            return FunctionCallInstruction(self, self.processInstruction(params[0]), params[1], *self.processStatements(params[2]))
            
    def processBlock(self, instruction):
        node, params = instruction
        if node == "IF":
            return IfInstruction(self, params[0], self.processInstruction(params[1]), self.processStatements(params[2]), self.processStatements(params[3]))
        elif node == "FOREVER":
            return ForeverInstruction(self, self.processStatements(params))
        elif node == "COUNT":
            return CountInstruction(self, self.processInstruction(params[1]), self.processStatements(params[0]))
        elif node == "WHILE":
            return WhileInstruction(self, self.processInstruction(params[0]), self.processStatements(params[1]))
        elif node == "FOR":
            return ForInstruction(self, params[0], self.processInstruction(params[1]), self.processStatements(params[2]))
    

    def parse(self, code):
        if not code.endswith("\n"):
            code += "\n" # dirty trailing newline hacks
        return self.parser.parse(self.lexer.tokenize(code))
    def interpret(self, ast):
        if not ast:
            return
        if self.debug:
            print("Parsed AST:", ast)
        return [self.processInstruction(i) for i in ast]
    def execute(self, instructions):
        if not instructions:
            return
        for i in instructions:
            i.execute(self.__context__)
    def run(self, code):
        self.execute(self.interpret(self.parse(code)))

