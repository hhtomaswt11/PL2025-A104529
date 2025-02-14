# Proibido usar modulo .csv do Python
import re

def parse_csv(filename):
    with open(filename, 'r', encoding='utf-8') as f:
        text = f.read()
    data = []      # Armazena todas as linhas (cada linha é uma lista de campos)
    row = []       # Campos da linha atual
    field = []     # Caracteres do campo atual
    in_quotes = False  # Flag para sabermos se estamos dentro de aspas
    i = 0
    length = len(text)

    while i < length:
        ch = text[i]

        if ch == '"':
            # Verifica se a próxima posição é outra aspa -> ""
            if i + 1 < length and text[i+1] == '"':
                # Verificamos se a próxima posição do texto contém outra aspa
                field.append('"')
                i += 2
                continue
            else:
                # Alterna se estamos dentro/fora de aspas
                in_quotes = not in_quotes

        elif (ch == ';') and (not in_quotes):
            # Delimitador fora de aspas -> fim do campo
            row.append(''.join(field))
            field = []

        elif (ch in ['\n', '\r']) and (not in_quotes):
            # Se encontramos new line fora de aspas -> fim da linha
            # Primeiro, fechamos o campo atual
            row.append(''.join(field))
            field = []
            # Adicionamos a linha completa à lista de linhas
            data.append(row)
            row = []

            # Se for "\r\n", saltamos o '\n' à frente
            if ch == '\r' and (i + 1 < length) and (text[i+1] == '\n'):
                i += 1

        else:
            # Caracter normal (ou delimitador dentro de aspas, ou \n dentro de aspas)
            # Fica dentro do campo!!
            field.append(ch)
        i += 1
    
    # Se sobrar algo no field/row no final do arquivo...
    if field or row:
        row.append(''.join(field))
        data.append(row)
    if data:   
        data.pop(0) # Tiramos o cabeçalho da lista resultante do parsing já que não será necessário usá-lo nos exercicíos propostos
    return data
