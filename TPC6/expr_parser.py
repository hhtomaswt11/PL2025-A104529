from expr_lexer import Lexer

class Parser:
    def __init__(self):
        self.lexer = Lexer()
        self.lexer.build()
        self.token_atual = None

    def erro(self):
        raise SyntaxError(f"Erro inesperado no token: {self.token_atual}")

    def proximo_token(self):
        self.token_atual = self.lexer.token()

    def fator(self):
        if self.token_atual and self.token_atual.type == 'NUMBER':
            valor = self.token_atual.value
            self.proximo_token()
            return valor
        self.erro()

    def termo(self):
        resultado = self.fator()
        while self.token_atual and self.token_atual.type == 'MULTIPLY':
            self.proximo_token()
            resultado *= self.fator()
        return resultado

    def expressao(self):
        resultado = self.termo()
        while self.token_atual and self.token_atual.type in ('PLUS', 'MINUS'):
            operador = self.token_atual.type
            self.proximo_token()
            if operador == 'PLUS':
                resultado += self.termo()
            else:
                resultado -= self.termo()
        return resultado

    def parse(self, texto):
        self.lexer.input(texto)
        self.proximo_token()
        return self.expressao()



if __name__ == "__main__":
    parser_instance = Parser()
    expressao = "5 + 3 * 2"
    print(f"Expressão: {expressao} = {parser_instance.parse(expressao)}")

    expressao2 = "2 * 7 - 5 * 3"
    print(f"Expressão: {expressao2} = {parser_instance.parse(expressao2)}")
