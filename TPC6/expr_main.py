from expr_parser import Parser

def main_fun():
    parser = Parser()

    expressoes = [
        "5 + 3 * 2",
        "2 * 7 - 5 * 3",
        "10 - 2 * 5",
        "8 + 4 * 3 - 2"
    ]
    resultados = []

    for expr in expressoes:
        resultado = parser.parse(expr)
        print(f"{expr} = {resultado}")
        resultados.append(f"{expr} = {resultado}")

    salvar = input("Guardar no ficheiro resultados.txt? (s/n): ").strip().lower()
    if salvar == 's':
        with open("resultados.txt", "w") as file:
            for linha in resultados:
                file.write(linha + "\n")
        print("Guardado em 'resultados.txt'")

if __name__ == "__main__":
    main_fun()
