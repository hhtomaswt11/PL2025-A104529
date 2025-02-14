from parse_csv import parse_csv


def obras_por_periodo(data):
    periodo_map = dict()
    for l in data:
        periodo = l[3]
        if periodo not in periodo_map: # Não existe no dict? 
            periodo_map[periodo] = 1 # Criámos a entrada e associamos o valor 1
        else:
            periodo_map[periodo] += 1 # Incrementamos o valor associado ao período
    return periodo_map





if __name__ == "__main__":
    filename = "obras.csv"
    content = parse_csv(filename)
    r = obras_por_periodo(content)
    print (r)
    