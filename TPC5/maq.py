import re, json

def carregar_json(filename):
        with open(filename, "r", encoding="utf-8") as file:
            return json.load(file)

def escrever_json(filename, stock):
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(stock, f, indent=4, ensure_ascii=False)

def get_produto(codigo, stock):
    if not re.fullmatch(r'\w+', codigo):  
        print("maq: Código de produto inválido.")
        return None

    for produto in stock:
        if produto["cod"] == codigo:
            return produto
    return None

def has_stock(stock):
    total = 0  
    for item in stock: 
        total += int(item['quant']) 
    return total > 0  
    
def get_stock(p):
    quant = p["quant"]
    if quant == 0:
        print ("Produto sem stock")
    return quant
    


def listar(stock):
    print("\nmaq:")
    print(f"{'cod':<10} | {'nome':<25} | {'quantidade':<10} | {'preço':<10}")
    print("-" * 60)
    for produto in stock:
        print(f"{produto['cod']:<10} | {produto['nome']:<25} | {produto['quant']:<10} | {produto['preco']:<10.2f}")


def processar_moedas_mensagem(mensagem):
    moedas_validas = {"2e": 200, "1e": 100, "50c": 50, "20c": 20, "10c": 10, "5c": 5, "2c": 2, "1c": 1}
    saldo = 0

    findall = re.findall(r'(\d+(?:e|c))', mensagem)
    # print(findall)
    # exit(1)
    for moeda in findall:
        if moeda in moedas_validas:
            saldo = saldo + moedas_validas[moeda]
        else:
            print("Formato de moeda inválido")
    #print(saldo)
    return saldo 

def converter_int_formato_moeda(saldo): # inteiro -> 3e30c
    euros = saldo // 100 
    centimos = saldo % 100  

    if euros > 0 and centimos > 0:
        return f"{euros}e{centimos}c"
    elif euros > 0:
        return f"{euros}e"
    elif centimos > 0:
        return f"{centimos}c"
    else:
        return "0c" 

def check_stock(p):
    if p["quant"] == 0:
        print("map: Produto sem stock")
        return False
    return True 
        
def selecionar_produto(produto, saldo, stock):

    if not check_stock(produto):
        return saldo

    preco_em_centimos = int(produto["preco"] * 100)

    if saldo < preco_em_centimos:
        print(f"maq: Saldo insuficiente para satisfazer o seu pedido")
        print(f"maq: Saldo = {converter_int_formato_moeda(saldo)}; Pedido = {converter_int_formato_moeda(preco_em_centimos)}")
        return saldo

    produto["quant"] -= 1
    saldo -= preco_em_centimos
    print(f"maq: Pode retirar o produto dispensado '{produto['nome']}'")
    print(f"maq: Saldo = {converter_int_formato_moeda(saldo)}") 
    return saldo


def devolver_troco(saldo):
    moedas_disponiveis = {"2e": 200, "1e": 100, "50c": 50, "20c": 20, "10c": 10, "5c": 5, "2c": 2, "1c": 1}
    troco = {}

    for moeda, valor in moedas_disponiveis.items():
        quantidade, saldo = divmod(saldo, valor)  
        if quantidade > 0:
            troco[moeda] = quantidade  

    if troco:
        troco_str = ", ".join(f"{v}x {k}" for k, v in troco.items())
        print(f"maq: Pode retirar o troco: {troco_str}.")


def conflito(cod, dados):
    for i in dados:
        if i['cod'].strip() == cod.strip():
            print (f'Produto com código {cod} já existe')
            return True 
    return False 
    

def adicionar_produto(stock):
    codigo = input("codigo do produto: ").strip()
    while conflito(codigo,stock):
        codigo= input("codigo do produto: ").strip()   
    nome = input("nome do produto: ").strip()
    quantidade = int(input("quantidade: ").strip())
    preco = float(input("preço: ").strip())

    stock.append({"cod": codigo, "nome": nome, "quant": quantidade, "preco": preco})
    print(f"maq: Produto '{nome}' adicionado ao stock.")


def atualizar_stock(produto, novo_stock):
    produto["quant"] = novo_stock

def maq(stock, filename):
    print("maq: Stock Carregado, Estado atualizado.")
    if not has_stock(stock):
        print("Máquina sem stock")
        
    print("maq: Bom dia. Estou disponível para atender o seu pedido.")
    saldo = 0
    while True:
        mensagem = input().strip()

        if mensagem == "LISTAR":
            listar(stock)
        elif mensagem.startswith("MOEDA"):
            # print("aqui")
            saldo += processar_moedas_mensagem(mensagem)
            formatted_saldo = converter_int_formato_moeda(saldo)
            print(f"maq: Saldo = {formatted_saldo}")
            
        elif mensagem.startswith("SELECIONAR"):
           # match = re.match(r'SELECIONAR\s*(\w+)', mensagem)
            match = re.match(r'(?i)selecionar\s*(\w+)', mensagem)

            if match:
                codigo = match.group(1)
                print(f'cod -> {codigo}')
                produto = get_produto(codigo, stock)
                if produto:
                    saldo = selecionar_produto(produto, saldo, stock)
                else:
                    print("maq: Produto não existe.")
            else:
                print ("ERROR")
        
        elif mensagem.startswith("ATUALIZAR_STOCK"):
            # match = re.match(r'ATUALIZAR_STOCK\s(\w+)\s(\d+)', mensagem)
            match = re.match(r'(?i)atualizar[_\s]stock\s+(\w+)\s+(\d+)', mensagem)

            if match:
                codigo = match.group(1)
                novo_stock = match.group(2)
                produto = get_produto(codigo, stock)
                if produto:
                    atualizar_stock(produto, novo_stock)
                else:
                    print("maq: Produto não existe")
            else:
                print("ERROR")     
        
        elif mensagem.startswith("CHECK_STOCK"):
            #match = re.match(r'CHECK_STOCK\s(\w+)', mensagem)
            match = re.match(r'(?i)check[_\s]stock\s+(\w+)', mensagem)

            if match:
                codigo = match.group(1)
                produto = get_produto(codigo, stock)   
                if produto: 
                 stock = get_stock(produto)
                 print(stock) 
                else:
                    print("maq: Produto não existe")
            else:
                print ("ERROR")
                
        elif mensagem == "SAIR":
            devolver_troco(saldo)
            print("maq: Até à próxima!")
            break

        elif mensagem == "ADICIONAR":
            adicionar_produto(stock)
        else:
            print("COMANDO NAO EXISTE. OPÇOES: LISTAR, MOEDA, SELECIONAR <cod>, SAIR, ADICIONAR, ATUALIZAR_STOCK <cod> <novo_stock>, CHECK_STOCK <cod>")


    escrever_json(filename, stock)






if __name__ == "__main__":
    filename = "stock.json"
    stock = carregar_json(filename)  
   # print(stock)
    maq(stock, filename) 
