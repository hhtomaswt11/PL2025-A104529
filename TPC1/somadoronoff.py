import re

def somador_on_off(texto):
    soma = 0
    ligado = True  # Começamos com a soma logo ligada 

    # FINDALL, de modo a retornar todas as ocorrências de um padrão (no caso, iremos filtrar por 'números', 'on', 'off' e '=')
    tokens = re.findall(r"\d+|on|off|=", texto, re.IGNORECASE)

    for token in tokens:
        if token.lower() == "off":
            ligado = False  
        elif token.lower() == "on":
            ligado = True  
        elif token == "=": # Retornamos a soma quando '=' é encontrado 
            print(f"-> {soma}") 
        elif ligado:  # Se estiver ativado, somamos os números
            soma += int(token)

# Test 
mensagem = "1iMRE6r=HtzkAon8o2sdXVtM0oLoffzNxZi3z2eqOpZNEqCJaLonK1mMTy4d89WoffaJ8uH6sgDxy2xMJoNRQZ7aAmkmhF5N923eTqqzequb4eYpA34DIojequZtnvw67LyrPxme0eqZbYZPon82fFbYKoffQXTonOnjjAAzS4=eq1tKe0VQuS89yuoffLoNCs8rV24P3Eeq1GeAtonjvTK0A5KmKAEaOon1=deqQcZrZ5MBu58HzkequWQ5XC9Fon83ctoffFHaEQFtN9aIonfjAq9eqW0L6F9W4=eq=2pOQRUgAM56DKoffZ6BYeq7sYononKZV=eq0K9KdW=VononAid6Uon6GeoffW=onD=OffonEQ=offG=39MoNyOn=EQOff7offOn5DSOffOn9OnW=43Uk=OffOnON"
mensagemSimples = "1a2b3c4d=on5e6f7g=off8h9i=on10j11k"

somador_on_off(mensagem)

