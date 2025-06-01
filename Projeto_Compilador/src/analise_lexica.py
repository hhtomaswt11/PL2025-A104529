import ply.lex as lex
import re 

class Lexer:
    """
    Analisador léxico. Divide o programa em tokens,
    """

    # Tokens
    tokens = [
         # símbolos e operadores especiais 
        'ID',
        'INTEGER',
        'REAL',
        'STRING',
        'PLUS',
        'MINUS',
        'TIMES',
        'DIVIDE',
        'LPAREN',
        'RPAREN',
        'LBRACKET',
        'RBRACKET',
        'SEMICOLON',
        'COLON',
        'COMMA',
        'PERIOD',
        'ASSIGN',
        'EQ',
        'NEQ',
        'LT',
        'GT',
        'LE',
        'GE',
        'APOSTROPHE',
        'COMMENT',
        
        # palavras-reservadas 
        'AND', 'ARRAY', 'BEGIN', 'CASE', 'CONST', 'DIV', 'DO', 'DOWNTO', 'ELSE', 'END',
        'FILE', 'FOR', 'FUNCTION', 'GOTO', 'IF', 'IN', 'LABEL', 'MOD', 'NIL', 'NOT',
        'OF', 'OR', 'PACKED', 'PROCEDURE', 'PROGRAM', 'RECORD', 'REPEAT', 'SET',
        'THEN', 'TO', 'TYPE', 'UNTIL', 'VAR', 'WHILE', 'WITH',
        'TRUE', 'FALSE', 'BOOLEAN', 'INTEGER_TYPE', 'REAL_TYPE', 'STRING_TYPE', 'CHAR_TYPE',
        'WRITELN', 'READLN', 'WRITE', 'READ', 'HALT'
    ]

    # Regexs 
    t_PLUS = r'\+'
    t_MINUS = r'-'
    t_TIMES = r'\*'
    t_DIVIDE = r'/'
    t_LPAREN = r'\('
    t_RPAREN = r'\)'
    t_LBRACKET = r'\['
    t_RBRACKET = r'\]'
    t_SEMICOLON = r';'
    t_COLON = r':'
    t_COMMA = r','
    t_PERIOD = r'\.'
    t_EQ = r'='
    t_NEQ = r'<>'
    t_LT = r'<'
    t_GT = r'>'
    t_LE = r'<='
    t_GE = r'>='
    t_APOSTROPHE = r'\''


    def t_INTEGER_TYPE(self, t):
        r'\binteger\b'
        return t

    def t_WRITELN(self, t):
        r'\bwriteln\b'
        return t

    def t_READLN(self, t):
        r'\breadln\b'
        return t

    def t_BOOLEAN(self, t):
        r'\bboolean\b'
        return t

    def t_STRING_TYPE(self, t):
        r'\bstring\b'
        return t

    def t_CHAR_TYPE(self, t):
        r'\bchar\b'
        return t

    def t_REAL_TYPE(self, t):
        r'\breal\b'
        return t

    def t_PROGRAM(self, t):
        r'\bprogram\b'
        return t

    def t_FUNCTION(self, t):
        r'\bfunction\b'
        return t

    def t_PROCEDURE(self, t):
        r'\bprocedure\b'
        return t

    def t_CONST(self, t):
        r'\bconst\b'
        return t

    def t_BEGIN(self, t):
        r'\bbegin\b'
        return t

    def t_END(self, t):
        r'\bend\b'
        return t

    def t_REPEAT(self, t):
        r'\brepeat\b'
        return t

    def t_UNTIL(self, t):
        r'\buntil\b'
        return t

    def t_WHILE(self, t):
        r'\bwhile\b'
        return t

    def t_DOWNTO(self, t):
        r'\bdownto\b'
        return t

    def t_RECORD(self, t):
        r'\brecord\b'
        return t

    def t_PACKED(self, t):
        r'\bpacked\b'
        return t

    def t_ARRAY(self, t):
        r'\barray\b'
        return t

    def t_WRITE(self, t):
        r'\bwrite\b'
        return t

    def t_READ(self, t):
        r'\bread\b'
        return t

    def t_AND(self, t):
        r'\band\b'
        return t

    def t_DIV(self, t):
        r'\bdiv\b'
        return t

    def t_MOD(self, t):
        r'\bmod\b'
        return t

    def t_NOT(self, t):
        r'\bnot\b'
        return t

    def t_FOR(self, t):
        r'\bfor\b'
        return t
    
    def t_XOR(self, t):
        r'\bxor\b'
        return t
    
    def t_OR(self, t):
        r'\bor\b'
        return t

    def t_IN(self, t):
        r'\bin\b'
        return t

    def t_IF(self, t):
        r'\bif\b'
        return t

    def t_DO(self, t):
        r'\bdo\b'
        return t

    def t_TO(self, t):
        r'\bto\b'
        return t

    def t_OF(self, t):
        r'\bof\b'
        return t

    def t_VAR(self, t):
        r'\bvar\b'
        return t

    def t_ELSE(self, t):
        r'\belse\b'
        return t

    def t_THEN(self, t):
        r'\bthen\b'
        return t

    def t_TYPE(self, t):
        r'\btype\b'
        return t

    def t_CASE(self, t):
        r'\bcase\b'
        return t

    def t_FILE(self, t):
        r'\bfile\b'
        return t

    def t_GOTO(self, t):
        r'\bgoto\b'
        return t

    def t_WITH(self, t):
        r'\bwith\b'
        return t

    def t_LABEL(self, t):
        r'\blabel\b'
        return t

    def t_SET(self, t):
        r'\bset\b'
        return t

    def t_NIL(self, t):
        r'\bnil\b'
        return t

    def t_TRUE(self, t):
        r'\btrue\b'
        return t

    def t_FALSE(self, t):
        r'\bfalse\b'
        return t

    def t_HALT(self, t):
        r'\bhalt\b'
        return t
    
    
    
    # ASSIGN 
    def t_ASSIGN(self, t):
        r':='
        return t
    
    # STRING
    def t_STRING(self, t):
        r"'[^']*'"
        t.value = t.value[1:-1]  
        return t


    # REAL
    def t_REAL(self, t):
        r'\d+\.\d+'
        t.value = float(t.value)
        return t

    # INTEGER
    def t_INTEGER(self, t):
        r'\d+'
        t.value = int(t.value)
        return t

    # ID 
    def t_ID(self, t):
        r'[a-zA-Z][a-zA-Z0-9_]*' # começa por um caractere alfabetico 
        return t

    # Comentarios 
    def t_COMMENT(self, t):
        r'\{[^}]*\}|\(\*[\s\S]*?\*\)'
        pass 

    t_ignore = ' \t'

    def t_newline(self, t):
        r'\n+'
        t.lexer.lineno += len(t.value)

    def t_error(self, t):
        print(f"Caractere ilegal '{t.value[0]}' na linha {t.lexer.lineno}")
        t.lexer.skip(1)
        
        
    # BUILD LEXER 
    def build(self, **kwargs):
        self.lexer = lex.lex(module=self, reflags=re.IGNORECASE, **kwargs)

        return self.lexer
    

    # reset
    def reset(self):
        self.lexer.lineno = 1



def create_lexer():
    lexer = Lexer()
    return lexer.build()