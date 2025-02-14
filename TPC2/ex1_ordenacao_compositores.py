from parse_csv import parse_csv


def ordem_alfabetica(lista):
    final = [] 
    for l in lista: 
        compositor = l[4]
        final.append(compositor) # Adicionar à lista de retorno
    final.sort()  # Ordenar a lista (basta usar o método sort())
    return final 





if __name__ == "__main__":
    filename = "obras.csv"
    content = parse_csv(filename)
    r = ordem_alfabetica(content)
    print (r)
    