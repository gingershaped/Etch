from sly import Lexer

class EtchLexer(Lexer):
    keywords = {
        IF,
        IS,
        IN,
        DO,
        OR,
        AS,
        FOR,
        AND,
        NOT,
        ELSE,
        DONE,
        OPEN,
        THEN,
        FROM,
        CLASS,
        WHILE,
        USING,
        TIMES,
        RETURN,
        DEFINE,
        FOREVER,
        BUILDER
    }
    symbols = {
        NEWLINE,
        ASSIGN,
        INCREMENT,
        DECREMENT,
        IP_ADD,
        IP_SUB,
        IP_MUL,
        IP_DIV,
        ADD,
        SUB,
        MUL,
        TRUEDIV,
        FLOORDIV,
        MOD,
        EXP,
        SWAP,
        COMPARE,
        LE,
        GE,
        LT,
        GT,
        NE,
        EQ,
        COLON,
        SEMICOLON,
        INTEGER,
        FLOAT,
        STRING,
        OPEN_SQ,
        CLOSE_SQ,
        OPEN_CB,
        CLOSE_CB,
        COMMA,
        ID,
    }
    tokens = set.union(keywords, symbols)
    ignore = " \t"
    ignore_comment = "~.*[;\n]"

    NEWLINE = r"\n+"

    OPEN_SQ = r"\["
    CLOSE_SQ = r"\]"
    OPEN_CB = r"\{"
    CLOSE_CB = r"\}"
    
    INCREMENT = r"\+\+"
    DECREMENT = r"--"

    IP_ADD = r"\+="
    IP_SUB = r"-="
    IP_MUL = r"\*="
    IP_DIV = r"/="
    
    ADD    = r'\+'
    SUB   = r'-'
    MUL   = r'\*'
    FLOORDIV = r'//'
    TRUEDIV  = r'/'
    MOD = r"%"
    EXP = r"\^"

    SWAP = r"><"
    COMPARE = r"<>"

    LE = r"<="
    GE = r">="
    LT = r"<"
    GT = r">"
    EQ = r"=="
    NE = r"!="
    
    ASSIGN = r"="
    COLON = r":"
    SEMICOLON = r";"
    COMMA = r","
    
    INTEGER = r'\d+'
    FLOAT = r'((\d*\.\d+)(E[\+-]?\d+)?|([1-9]\d*E[\+-]?\d+))'
    STRING = r'[\"\'](\\.|[^"\'\\])*[\"\']'
    

    def INTEGER(self, t):
        t.value = int(t.value)
        return t
    def FLOAT(self, t):
        t.value = float(t.value)
        return t
    def STRING(self, t):
        t.value = t.value[1:-1]
        return t
    def NEWLINE(self, t):
        self.lineno += len(t.value)
        return t

    ID = r':?[a-zA-Z_][a-zA-Z0-9_]*'

    ID["if"] = IF
    ID["is"] = IS
    ID["in"] = IN
    ID["or"] = OR
    ID["do"] = DO
    ID["as"] = AS
    ID["and"] = AND
    ID["not"] = NOT
    ID["for"] = FOR
    ID["then"] = THEN
    ID["else"] = ELSE
    ID["open"] = OPEN
    ID["from"] = FROM
    ID["done"] = DONE
    ID["while"] = WHILE
    ID["class"] = CLASS
    ID["using"] = USING
    ID["times"] = TIMES
    ID["return"] = RETURN
    ID["define"] = DEFINE
    ID["forever"] = FOREVER
    ID["builder"] = BUILDER