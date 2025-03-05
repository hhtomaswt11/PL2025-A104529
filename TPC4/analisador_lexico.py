import ply.lex, re 

tokens = [
    'CMD_SELECT',
    'CMD_WHERE',
    'CMD_LIMIT',
    'BLOCK_START',
    'BLOCK_END',
    'SEPARATOR',
    'COMMENTARY',
    'IDENTIFIER',
    'INTEGER',
    'TEXT_VALUE',
    'RELATION'
]

t_ignore = ' \t'

def t_error(t):
    print(f'Char não reconhecido"')
    t.lexer.input(t.value[1:])

def t_BLOCK_START(t):
    r'\{'
    return t

def t_BLOCK_END(t):
    r'\}'
    return t

def t_SEPARATOR(t):
    r'\.' 
    return t

def t_COMMENTARY(t):
    r'\#.*' 
    return t

def t_IDENTIFIER(t):
    r'\?\w+'  
    return t

def t_CMD_SELECT(t):
    r'(?i:\bSELECT\b)'
    return t

def t_CMD_WHERE(t):
    r'(?i:\bWHERE\b)'
    return t

def t_CMD_LIMIT(t):
    r'(?i:\bLIMIT\b)' 
    return t

def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

def t_INTEGER(t):
    r'\d+'
    match = re.match(r'\d+', t.value)  # captura o numero explicitamente
    if match:
        t.value = int(match.group())  # converte a correspondencia para int 
    return t

def t_TEXT_VALUE(t):
    r'"[^"]*"(?:@\w{2,})?' 
    return t

def t_RELATION(t):
    r'[a-zA-Z_][\w:]*'  
    return t

def analisador_lexico(input_code):
    lexer = ply.lex.lex() 
    lexer.input(input_code)

    for tk in lexer:
        print(f'Tipo: {tk.type}, Valor: {tk.value}, Linha: {tk.lineno}')


if __name__ == "__main__":
    
    test_query = '''
    # DBPedia: Informações sobre Chuck Berry
    SELECT ?nome ?descricao WHERE {
        ?s a dbo:MusicalArtist.
        ?s foaf:name "Chuck Berry"@en .
        ?obra dbo:artist ?s.
        ?obra foaf:name ?nome.
        ?obra dbo:abstract ?descricao
    } LIMIT 1000
    '''
    
    test_query2= '''
    # DBPedia: obras de Chuck Berry
    select ?nome ?desc where {
    ?s a dbo:MusicalArtist.
    ?s foaf:name "Chuck Berry"@en .
    ?w dbo:artist ?s.
    ?w foaf:name ?nome.
    ?w dbo:abstract ?desc
    } LIMIT 1000
    '''
    
    analisador_lexico(test_query2)
