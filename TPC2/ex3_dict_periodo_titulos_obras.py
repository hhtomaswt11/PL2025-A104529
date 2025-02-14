from parse_csv import parse_csv


def dict_periodo_titulos(data):
    dic = dict()
    for l in data:
        periodo = l[3]
        titulo = l[0]
        if periodo not in dic:
            dic[periodo] = list() # Criámos uma lista associada ao período caso este ainda não este presente no dict
          
        dic[periodo].append(titulo) # Adicionamos o título à lista associada ao período
    return dic 





if __name__ == "__main__":
    filename = "obras.csv"
    content = parse_csv(filename)
    r = dict_periodo_titulos(content)
    print (r)
    