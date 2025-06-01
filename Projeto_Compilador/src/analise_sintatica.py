import ply.yacc as yacc
from src.analise_lexica import Lexer, create_lexer
from src.tabela_simbolos import SymbolTable


class Node:
    """Classe base para nós da Árvore Sintática Abstrata (AST)."""
    def __init__(self, type, children=None, leaf=None):
        self.type = type            # Tipo do nó - integer, binary_op, etc 
        self.children = children if children else []  # filhos do nó - operandos de uma operação, etc
        self.leaf = leaf            # Valor da folha, se for uma folha - valor literal 'x' '2' '4', etc
    
    def __repr__(self):
        return f"{self.type}({self.leaf if self.leaf is not None else ''})"


class Parser:
    """
    Analisador sintático. Cria a AST a partir dos tokens.
    """
    
    def __init__(self):
        self.lexer = create_lexer()
        self.tokens = Lexer.tokens
        self.symtab = SymbolTable()
        self.errors = []
        self.parser = yacc.yacc(module=self) # inicializa o parser. cria o parser ao compilar as regras p_ 
        
    # Regra para a unidade de programa completa
    def p_program(self, p):
        '''program : PROGRAM ID SEMICOLON block PERIOD'''
        p[0] = Node('program', [p[4]], p[2])
    
    # Regra para blocos (estrutura básica do programa)
    def p_block(self, p):
        '''block : declarations compound_statement'''
        p[0] = Node('block', [p[1], p[2]])

    def p_declarations(self, p):
        '''declarations : VAR var_declarations
                        | function_declaration
                        | empty'''
        if len(p) == 3:
            p[0] = Node('declarations', [p[2]])
        elif p[1] is not None:
            p[0] = Node('declarations', [p[1]])
        else:
            p[0] = Node('declarations')
        
    def p_function_block(self, p):
        '''function_block : VAR var_declarations compound_statement
                        | compound_statement'''
        if len(p) == 4:
            # VAR declarações + begin...end
            p[0] = Node('block', [Node('declarations', [p[2]]), p[3]])
        else:
            # só begin...end
            p[0] = Node('block', [Node('declarations'), p[1]])


    def p_declaration(self, p):
        '''declaration : VAR var_declarations
                    | function_declaration'''
        p[0] = p[2] if p[1].lower() == 'var' else p[1]

    # Regra para declarações de variáveis
    def p_var_declarations(self, p):
        '''var_declarations : var_declarations var_declaration
                           | var_declaration'''
        if len(p) > 2:
            p[1].children.append(p[2])
            p[0] = p[1]
        else:
            p[0] = Node('var_declarations', [p[1]])
    
    # Regra para uma única declaração de variável
    def p_var_declaration(self, p):
        '''var_declaration : id_list COLON type_spec SEMICOLON'''
        p[0] = Node('var_declaration', [p[1], p[3]])
        
        # Adiciona as variáveis na tabela de símbolos
        var_type = p[3].leaf
        for var_id in p[1].children:
            self.symtab.add_symbol(var_id.leaf, var_type, kind="variable")
    
    # Regra para lista de identificadores
    def p_id_list(self, p):
        '''id_list : id_list COMMA ID
                  | ID'''
        if len(p) > 2:
            p[1].children.append(Node('id', leaf=p[3]))
            p[0] = p[1]
        else:
            p[0] = Node('id_list', [Node('id', leaf=p[1])])
    
    # Regra para especificação de tipos
    def p_type_spec(self, p):
        '''type_spec : INTEGER_TYPE
                     | REAL_TYPE
                     | BOOLEAN
                     | STRING_TYPE
                     | CHAR_TYPE
                     | array_type'''
        if len(p) == 2:
            if isinstance(p[1], Node): # Se for um array_type
                p[0] = p[1]
            else:
                p[0] = Node('type', leaf=p[1])
    
    # Regra para tipos de array
    def p_array_type(self, p):
        '''array_type : ARRAY LBRACKET INTEGER PERIOD PERIOD INTEGER RBRACKET OF type_spec'''
        p[0] = Node('array_type', [Node('range', [Node('integer', leaf=p[3]), Node('integer', leaf=p[6])]), p[9]])
    
    # Regra para bloco de comandos
    def p_compound_statement(self, p):
        '''compound_statement : BEGIN statement_list END'''
        p[0] = Node('compound', [p[2]])
    
    # Regra para lista de comandos
    def p_statement_list(self, p):
        '''statement_list : statement_list SEMICOLON statement
                         | statement'''
        if len(p) > 2:
            if p[3] is not None:  # Ignorar comandos vazios
                p[1].children.append(p[3])
            p[0] = p[1]
        else:
            if p[1] is not None:  # Ignorar comandos vazios
                p[0] = Node('statement_list', [p[1]])
            else:
                p[0] = Node('statement_list')
    
    # Regra para um único comando
    def p_statement(self, p):
        '''statement : compound_statement
                     | assignment_statement
                     | if_statement
                     | while_statement
                     | for_statement
                     | procedure_call_statement
                     | halt_statement
                     | empty'''
        p[0] = p[1]
    
    # Regra para comando de atribuição
    def p_assignment_statement(self, p):
        '''assignment_statement : variable ASSIGN expression'''
        p[0] = Node('assignment', [p[1], p[3]])
    
    def p_variable(self, p):
        '''variable : ID
                | ID LBRACKET expression RBRACKET''' # arrays 
        if len(p) > 2:
            p[0] = Node('array_access', [p[3]], leaf=p[1])
        else:
            p[0] = Node('variable', leaf=p[1])
            

    # Regra para comando if-then-else
    def p_if_statement(self, p):
        '''if_statement : IF expression THEN statement
                        | IF expression THEN statement ELSE statement'''
                        
        if len(p) > 5:
            p[0] = Node('if', [p[2], p[4], p[6]])
        else:
            p[0] = Node('if', [p[2], p[4]])
    
    # Regra para comando while
    def p_while_statement(self, p):
        '''while_statement : WHILE expression DO statement'''
        p[0] = Node('while', [p[2], p[4]])

    # Regra para comando for
    def p_for_statement(self, p):
        '''for_statement : FOR ID ASSIGN expression TO expression DO statement
                        | FOR ID ASSIGN expression DOWNTO expression DO statement'''
        direction = 'to' if p[5] == 'to' else 'downto'
        p[0] = Node('for', [Node('id', leaf=p[2]), p[4], p[6], p[8]], direction)
    
    # Regra para chamada de procedimento
    # def p_procedure_call_statement(self, p):
    #     '''procedure_call_statement : ID LPAREN expression_list RPAREN
    #                                | ID LPAREN RPAREN
    #                                | WRITELN LPAREN expression_list RPAREN
    #                                | WRITELN LPAREN RPAREN
    #                                | READLN LPAREN variable RPAREN
    #                                | READLN LPAREN RPAREN'''
    #     if p[1].lower() in ('writeln', 'readln'):
    #         if len(p) > 4:
    #             if p[1].lower() == 'writeln':
    #                 p[0] = Node('writeln', [p[3]])
    #             else:  # readln
    #                 p[0] = Node('readln', [p[3]])
    #         else:
    #             p[0] = Node(p[1].lower(), [])
    #     else:
    #         if len(p) > 4:
    #             p[0] = Node('procedure_call', [Node('id', leaf=p[1]), p[3]])
    #         else:
    #             p[0] = Node('procedure_call', [Node('id', leaf=p[1])])
    
    
    
    def p_procedure_call_statement(self, p):
        '''procedure_call_statement : ID LPAREN expression_list RPAREN
                                | ID LPAREN RPAREN
                                | WRITELN LPAREN expression_list RPAREN
                                | WRITELN LPAREN RPAREN
                                | WRITE LPAREN expression_list RPAREN
                                | WRITE LPAREN RPAREN
                                | READLN LPAREN variable RPAREN
                                | READLN LPAREN RPAREN'''
        if p[1].lower() in ('writeln', 'write', 'readln'):
            if len(p) > 4:
                if p[1].lower() == 'writeln':
                    p[0] = Node('writeln', [p[3]])
                elif p[1].lower() == 'write':
                    p[0] = Node('write', [p[3]])
                else:  # readln
                    p[0] = Node('readln', [p[3]])
            else:
                p[0] = Node(p[1].lower(), [])
        else:
            if len(p) > 4:
                p[0] = Node('procedure_call', [Node('id', leaf=p[1]), p[3]])
            else:
                p[0] = Node('procedure_call', [Node('id', leaf=p[1])])

    
    def p_expression_list(self, p):
        '''expression_list : expression_list COMMA expression
                       | expression'''
        if len(p) > 2:
              p[1].children.append(p[3])
              p[0] = p[1]
        else:
             p[0] = Node('expression_list', [p[1]])


    # Regra para expressões
    def p_expression(self, p):
        '''expression : simple_expression
                     | simple_expression relop simple_expression'''
        if len(p) > 2:
            p[0] = Node('binary_op', [p[1], p[3]], p[2])
        else:
            p[0] = p[1]
    
    # Regra para operadores relacionais
    def p_relop(self, p):
        '''relop : EQ
                | NEQ
                | LT
                | LE
                | GT
                | GE
                | IN'''
        p[0] = p[1]
    
    # Regra para expressões simples
    def p_simple_expression(self, p):
        '''simple_expression : term
                            | simple_expression addop term'''
        if len(p) > 2:
            p[0] = Node('binary_op', [p[1], p[3]], p[2])
        else:
            p[0] = p[1]
    
    # Regra para operadores de adição
    def p_addop(self, p):
        '''addop : PLUS
                | MINUS
                | OR'''
        p[0] = p[1]
    
    # Regra para termos
    def p_term(self, p):
        '''term : factor
                | term mulop factor'''
        if len(p) > 2:
            p[0] = Node('binary_op', [p[1], p[3]], p[2])
        else:
            p[0] = p[1]
    
    # Regra para operadores de multiplicação
    def p_mulop(self, p):
        '''mulop : TIMES
                | DIVIDE
                | DIV
                | MOD
                | AND'''
        p[0] = p[1]
    
    # Regra para fatores
    def p_factor(self, p):
        '''factor : variable
                 | INTEGER
                 | REAL
                 | STRING
                 | TRUE
                 | FALSE
                 | LPAREN expression RPAREN
                 | NOT factor
                 | function_call'''
        if len(p) == 2:
            if isinstance(p[1], Node):  # Se for uma variável ou chamada de função
                p[0] = p[1]
            elif isinstance(p[1], int):
                p[0] = Node('integer', leaf=p[1])
            elif isinstance(p[1], float):
                p[0] = Node('real', leaf=p[1])
            elif p[1] in ('true', 'false'):
                p[0] = Node('boolean', leaf=p[1])
            else:
                p[0] = Node('string', leaf=p[1])
        elif len(p) == 3:  # NOT factor
            p[0] = Node('unary_op', [p[2]], p[1])
        else:  # LPAREN expression RPAREN
            p[0] = p[2]
    
    def p_formatted_expression(self,p): # NOVO 
        '''expression : variable COLON INTEGER
                    | variable COLON INTEGER COLON INTEGER'''
        if len(p) == 4:
            p[0] = Node('formatted_output', [p[1], Node('integer', leaf=p[3])])
        else:
            p[0] = Node('formatted_output', [p[1], Node('integer', leaf=p[3]), Node('integer', leaf=p[5])])
    

    # Regra para chamada de função
    def p_function_call(self, p):
        '''function_call : ID LPAREN expression_list RPAREN
                        | ID LPAREN RPAREN'''
        if len(p) > 4:
            p[0] = Node('function_call', [Node('id', leaf=p[1]), p[3]])
        else:
            p[0] = Node('function_call', [Node('id', leaf=p[1])])
    

    def p_function_declaration(self, p):
        '''function_declaration : FUNCTION ID LPAREN param_list RPAREN COLON type_spec SEMICOLON function_block SEMICOLON'''
        p[0] = Node('function_decl', [Node('id', leaf=p[2]), p[4], p[7], p[9]])

            
    def p_param_list(self, p):
        '''param_list : param_list SEMICOLON param
                    | param'''
        if len(p) > 2:
            p[1].children.append(p[3])
            p[0] = p[1]
        else:
            p[0] = Node('param_list', [p[1]])

    def p_param(self, p):
        '''param : id_list COLON type_spec'''
        p[0] = Node('param', [p[1], p[3]])
        
        
    # Regra para comando halt
    def p_halt_statement(self, p):
        '''halt_statement : HALT SEMICOLON'''
        p[0] = Node('halt')


    # Regra para produções vazias
    def p_empty(self, p):
        'empty :'
        p[0] = None
        
    # Tratamento de erros
    def p_error(self, p):
        if p:
            error_msg = f"Erro de sintaxe na linha {p.lineno}, token '{p.value}'"
            self.errors.append(error_msg)
            print(error_msg)
        else:
            self.errors.append("Erro de sintaxe: fim inesperado do ficheiro")
            print("Erro de sintaxe: fim inesperado do ficheiro")
            

    # Método para analisar uma string
    def parse(self, data):
        self.errors = []
        return self.parser.parse(data, lexer=self.lexer) 
    # Inicia a análise léxica e sintática ao mesmo tempo
    # O texto é entregue ao lexer, que transforma em TOKENS com base nas regras t_
    # Com base nos tokens, o parser tenta casa-los com alguma regra p_. Se casar, a árvore AST começa a ser construída. 
    # Cada regra retorna um Node, atribuindo-o a p[0]
    # No fim da analise, o valor de p[0] na regra inicial p_program é o que é retornado
    # É aplicada uma análise semantica sobre a AST, recursivamente 
    # Retorna a AST 
    
    


# Função para criar uma instância do parser
def create_parser():
    return Parser()



