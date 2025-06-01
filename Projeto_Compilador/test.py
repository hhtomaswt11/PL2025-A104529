import sys
from src.analise_sintatica import create_parser
from src.analise_lexica import create_lexer
from src.analise_semantica import SemanticAnalyzer

def print_ast(node, indent=0):
    if node is None:
        return
    print("  " * indent + f"{node.type}: {node.leaf}")
    for child in node.children:
        print_ast(child, indent + 1)

def run_tokenizer(source_code):
    """Executa o lexer e imprime todos os tokens."""
    lexer = create_lexer()
    lexer.input(source_code)
    for tok in lexer:
        print(tok)

def run_ast(source_code):
    """Executa o parser e imprime a AST se válida."""
    parser = create_parser()
    ast = parser.parse(source_code)
    if ast:
        print("AST:")
        print_ast(ast)
        print("Análise sintática concluída com sucesso!")
    else:
        print("Erros na análise sintática:")
        for error in parser.errors:
            print(f"  - {error}")

def run_semantic(source_code):
    """Executa o parser + análise semântica."""
    parser = create_parser()
    ast = parser.parse(source_code)
    if not ast:
        print("Erro: análise sintática falhou. Análise semântica não realizada.")
        for error in parser.errors:
            print(f"  - {error}")
        return

    analyzer = SemanticAnalyzer()
    success = analyzer.analyze(ast)
    if not success:
        print("Análise semântica falhou.")
        for e in analyzer.errors:
            print(" -", e)
    else:
        print("Análise semântica concluída com sucesso!")


if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Comando correto: python main.py <ficheiro.pas> <modo>")
        print("Modos: tokens | ast | semantic")
        sys.exit(1)

    pascal_file = sys.argv[1]
    mode = sys.argv[2].lower()

    with open(pascal_file, 'r') as file:
        source_code = file.read()

    if mode == "tokens":
        run_tokenizer(source_code)
    elif mode == "ast":
        run_ast(source_code)
    elif mode == "semantic":
        run_semantic(source_code)
    elif mode == "all":
        run_tokenizer(source_code)
        print('\n')
        run_ast(source_code)
        print('\n')
        run_semantic(source_code)
    else:
        print(f"Modo desconhecido: '{mode}'. Usar 'tokens', 'ast' ou 'semantic'.")
