import re 

def substituir_cabecalho(match):
    nivel = len(match.group(1))  
    conteudo = match.group(2)   
    return f"<h{nivel}>{conteudo}</h{nivel}>"

def substituir_negrito(match):
    conteudo = match.group(1)
    return f"<b>{conteudo}</b>"

def substituir_italico(match):
    conteudo = match.group(1)
    return f"<i>{conteudo}</i>"

def link(match):
    content = match.group(1)
    #print (f'conteudo: {content}')
    referencia = match.group(2)
    #print(f'ref: {referencia}')
    link_referencia = match.group(3)
    #print(f'link ref: {link_referencia}')
    return f'{content} <a href="{link_referencia}">{referencia}</a>'
    
def imagem(match):
    inicial = match.group(1)
    referencia = match.group(2)
    link = match.group(3)
    final = match.group(5)
        
    return f'{inicial}<img src="{link}" alt="{referencia}"/> {final}'
    
def criar_lista(match): 
    value = match.group(2)
    return f'<li>{value}</li>'
      
    
    
def conversor(data):
    output = []
    
    linhas = data.splitlines()
    
    padrao_hash = r"^(#{1,6})\s+(.+)" 
      
    padrao_bold = r"\*\*(.+?)\*\*" 
    
    padrao_italico = r"\*(.+?)\*"
    
    padrao_link = r"([A-Za-z0-9\:\,\;\%\&\$\/ ]+)\s*\[([\w ]+)\]\s*\((https?\:\/\/[A-Za-z]+\.[A-Za-z]+\.[A-Za-z]{2,})\)"
    
    padrao_imagem = r"([^\!]*)\s*\!\[([^\]]+)\]\s*\((https?:\/\/[^\s)]+\.([A-Za-z]{2,}))\)(.*)"
    
    padrao_lista = r"^\s*(\d+)\.\s*(.+)"
    
    # [^\]]+ corresponde a qualquer coisa exceto ]
    # [^\.]+ corresponde a qualquer coisa exceto . 
    
    i = 0 
    while i < len(linhas):
        linha = linhas[i].strip()
        
        if re.match(padrao_hash, linha):
            linha_convertida = re.sub(padrao_hash, substituir_cabecalho, linha)
            output.append(linha_convertida )
            i = i+1 
        
        elif re.search(padrao_bold, linha):
            linha_convertida = re.sub(padrao_bold, substituir_negrito, linha)
            output.append(linha_convertida )
            i = i+1
            
        elif re.search(padrao_italico, linha):
            linha_convertida = re.sub(padrao_italico, substituir_italico, linha)
            output.append(linha_convertida )
            i = i+1
            
        elif re.search(padrao_link, linha):
            linha_convertida = re.sub(padrao_link, link , linha)
            output.append(linha_convertida )
            i = i+1
            
        elif re.search(padrao_imagem, linha):
            linha_convertida = re.sub(padrao_imagem, imagem, linha)
            output.append(linha_convertida )
            i= i+1
            
        elif re.search(padrao_lista, linha):
            output.append("<ol>" )
            while(i < len(linhas) and re.search(padrao_lista, linhas[i])):
                linha_convertida = re.sub(padrao_lista, criar_lista, linhas[i])
                output.append(linha_convertida )
                i +=1
            output.append("</ol>" )
        else: 
            output.append(linha)
            i = i+1                                 
          
    return "\n".join(output)

def abrir_ler_ficheiro(filename):
    with open (filename, 'r') as f:
        content = f.read()
    return content 


def abrir_escrever_ficheiro(filename, msg):
    with open (filename, 'w') as f:    
        f.write(msg)

           
# "       
# 1. Primeiro item   
# 2. Segundo item          
# "    

# Tests 
markdown_texto = """
# Titulo Principal
## Subtítulo
### Seção 1
#### Sub-seção 1.1
##### Sub-seção 1.1.1
###### Sub-seção 1.1.1.1
Texto normal aqui.
"""

markdown_texto2 = """
# Titulo Principal
Este é um **exemplo**
Este é um *exemplo*
"""

markdown_texto3 = """
Como se vê na imagem: ![imagem dum coelho](http://www.coellho.com) Continuação 
Como se vê na imagem seguinte: ![imagem dum coelho](http://www.coellho.com) ...
"""

markdown_texto4 = """
1. Primeiro item
2. Segundo item
"""


markdown_texto5 = """
2. Segundo item
"""

markdown_texto6 = """
# Texto N1
## Texto N2
### Texto N3
A negrito: **negrito**
Em Italico: *italico*
1. Primeiro item
2. Segundo item
3. Terceiro item
4. Quarto item 
O link pode ser consultado em [Processamento de Linguagens] (https://www.pl.pt)
Consulte na seguinte imagem: ![Processamento de Linguagens] (https://www.pl.pt)
"""


if __name__ == "__main__":
    filename_input = "EXEMPLO.md"
    filename_output = "EXEMPLO.html"
    content = abrir_ler_ficheiro(filename_input)
    html_format = conversor(content)
    abrir_escrever_ficheiro(filename_output, html_format)
    print(conversor(markdown_texto6))
















