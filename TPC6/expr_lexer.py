import ply.lex as lex

class Lexer:
    tokens = ('NUMBER', 'PLUS', 'MINUS', 'MULTIPLY')

    t_PLUS = r'\+'
    t_MINUS = r'-'
    t_MULTIPLY = r'\*'
    t_ignore = ' \t'

    def t_NUMBER(self, t):
        r'\d+'
        t.value = int(t.value)  
        return t

    def t_newline(self, t):
        r'\n+'
        t.lexer.lineno += len(t.value)

    def t_error(self, t):
        print(f"Caractere inválido: {t.value[0]}. Linha {t.lexer.lineno}")
        t.lexer.skip(1)

    def build(self):
        self.lexer = lex.lex(module=self)

    def input(self, text):
        self.lexer.input(text)

    def token(self):
        return self.lexer.token()



if __name__ == "__main__":
    lex_instance = Lexer()
    lex_instance.build()
    lex_instance.input("3 + 4 * 2 - 7")

    while (tok := lex_instance.token()):
        print(tok)
