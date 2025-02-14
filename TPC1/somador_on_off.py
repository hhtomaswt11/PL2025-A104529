

def somador_on_off(texto):
    soma = 0
    ligado = True  # Começamos com a soma logo ligada
    num_temp = ""  # Armazenamos os números ao longo da iteração 
    if not texto.endswith('='):
        texto += '='

    for i in range(len(texto)): 
        char = texto[i]

        if char.isdigit():  # Filtrar os números 
            num_temp += char # Vamos criando o número ao longo das iterações. Quando não for detetado um número e a soma estiver ligada, adicionamos esse número à soma 
        elif num_temp:  # Se o número for diferente de "" e ligado, então somamos
            if ligado:
                soma += int(num_temp)  
            num_temp = ""  # Reset do número 

        # Verificamos 'on' e 'off' na string 
        if texto[i:i+2].lower() == "on":
            ligado = True  
            i += 1  # Passar um caractere à frente ('n') de 'on'
        elif texto[i:i+3].lower() == "off":
            ligado = False  
            i += 2  # Passar dois caracteres à frente ('ff') de 'off'

        if char == "=": 
            print(f"{soma}")

    # Caso em que sobra um número no final da string, somamos também 
    if num_temp and ligado:
        soma += int(num_temp)

if __name__ == "__main__":
    # Test
    mensagem = "1iMRE6r=HtzkAon8o2sdXVtM0oLoffzNxZi3z2eqOpZNEqCJaLonK1mMTy4d89WoffaJ8uH6sgDxy2xMJoNRQZ7aAmkmhF5N923eTqqzequb4eYpA34DIojequZtnvw67LyrPxme0eqZbYZPon82fFbYKoffQXTonOnjjAAzS4=eq1tKe0VQuS89yuoffLoNCs8rV24P3Eeq1GeAtonjvTK0A5KmKAEaOon1=deqQcZrZ5MBu58HzkequWQ5XC9Fon83ctoffFHaEQFtN9aIonfjAq9eqW0L6F9W4=eq=2pOQRUgAM56DKoffZ6BYeq7sYononKZV=eq0K9KdW=VononAid6Uon6GeoffW=onD=OffonEQ=offG=39MoNyOn=EQOff7offOn5DSOffOn9OnW=43Uk=OffOnON"
    mensagemSimples = "1a2b3c4d=on5e6f7g=off8h9i=on10j11k"
    somador_on_off(mensagem)