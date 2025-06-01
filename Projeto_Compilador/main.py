import sys, os
from src.analise_sintatica import create_parser
from src.analise_semantica import SemanticAnalyzer
from src.otimizar_AST import collect_used_variables, prune_unused_var_declarations
from src.codegen import CodeGenerator
from vm import VirtualMachine
from colorama import init
init(autoreset=True)

def main(pascal_file):
    with open(pascal_file, 'r') as file:
        source_code = file.read()

    # Análise sintática
    parser = create_parser()
    ast = parser.parse(source_code)
    
    used_vars = collect_used_variables(ast)
    prune_unused_var_declarations(ast, used_vars)

    if parser.errors:
        print("Erros de parsing:")
        for e in parser.errors:
            print(" -", e)
        return

    #print("--- Análise sintática concluída ---")

    # Análise semântica
    analyzer = SemanticAnalyzer()
    success = analyzer.analyze(ast)
    if not success:
        print("Erros semânticos encontrados:")
        for e in analyzer.errors:
            print(" -", e)
        return

    #print("--- Análise semântica concluída ---")

    # Code generator 
    generator = CodeGenerator(analyzer.symtab)
    code = generator.generate(ast)




    filename = os.path.basename(pascal_file).replace(".pas", ".vm")
    output_dir = os.path.join("examples", "vm")
    os.makedirs(output_dir, exist_ok=True)
    output_file = os.path.join(output_dir, filename)

    with open(output_file, "w") as f:
        for line in code:
            f.write(line + "\n")

    #print(f"\nCódigo gerado em: {output_file}")

    vm = VirtualMachine()
    vm.load_code(code)
    vm.run()




if __name__ == "__main__":
    if len(sys.argv) != 2: 
        print("Comando correto: python3 main.py <ficheiro.pas>")
    else:
        pascal_file = sys.argv[1]
        main(pascal_file)     # python3 main.py examples/pas/hello.pas
