from src.analise_sintatica import Node

def collect_used_variables(node, used_vars=None):
    if used_vars is None:
        used_vars = set()

    if node is None:
        return used_vars

    if node.type == 'variable' or node.type == 'array_access':
        used_vars.add(node.leaf)
    elif node.type == 'assignment':
        if node.children[0].type == 'variable':
            used_vars.add(node.children[0].leaf)

    for child in node.children:
        collect_used_variables(child, used_vars)

    return used_vars


def prune_unused_var_declarations(node, used_vars):
    if node is None or not node.children:
        return

    # Verifica se este é um bloco de declarações de variáveis
    if node.type == 'var_declarations':
        new_children = []
        for decl in node.children:
            if decl.type == 'var_declaration':
                id_list_node = decl.children[0]
                type_node = decl.children[1]

                # Filtra variáveis usadas
                new_ids = [id_node for id_node in id_list_node.children if id_node.leaf in used_vars]
                if new_ids:
                    # Se ainda sobrou alguma variável, mantém o nó
                    new_id_list_node = Node('id_list', new_ids)
                    new_children.append(Node('var_declaration', [new_id_list_node, type_node]))

            else:
                new_children.append(decl)

        node.children = new_children

    # Recursivamente percorre a árvore
    for child in node.children:
        prune_unused_var_declarations(child, used_vars)
