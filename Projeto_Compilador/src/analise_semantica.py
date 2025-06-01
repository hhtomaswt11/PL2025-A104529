from src.tabela_simbolos import SymbolTable

class SemanticAnalyzer:
    def __init__(self):
        self.symtab = SymbolTable()
        self.errors = []
        self.warnings = []
        self.current_scope = None

    def analyze(self, ast):
        if ast is None:
            return False
        self._analyze_node(ast)
        return len(self.errors) == 0

    def _analyze_node(self, node):
        if node is None:
            return None

        method_name = f"_analyze_{node.type}"
        method = getattr(self, method_name, None)
        if method:
            return method(node)
        else:
            for child in node.children:
                self._analyze_node(child)

    def _analyze_program(self, node):
        return self._analyze_node(node.children[0])

    def _analyze_block(self, node):
        for child in node.children:
            self._analyze_node(child)

    def _analyze_declarations(self, node):
        for child in node.children:
            self._analyze_node(child)

    def _analyze_var_declarations(self, node):
        for child in node.children:
            self._analyze_node(child)

    def _analyze_var_declaration(self, node):
        id_list, type_node = node.children
        var_type = type_node.leaf
        

        if var_type == "string_bounded":
            str_len = type_node.children[0].leaf
            for var in id_list.children:
                self.symtab.add_symbol(var.leaf, type="string", kind="variable", size=int(str_len))
        else:
            for var in id_list.children:
                if type_node.type == "array_type":
                    # Pega informações do array
                    range_node = type_node.children[0]
                    base_type = type_node.children[1].leaf

                    lower_bound = int(range_node.children[0].leaf)
                    upper_bound = int(range_node.children[1].leaf)
                    size = upper_bound - lower_bound + 1

                    self.symtab.add_symbol(
                        var.leaf,
                        type="array",
                        kind="variable",
                        size=size,
                        dimensions=(lower_bound, upper_bound),
                        element_type=base_type
                    )
                else:
                    self.symtab.add_symbol(var.leaf, var_type, kind="variable")

            
    def _analyze_function_decl(self, node):
        func_id = node.children[0].leaf
        param_list = node.children[1]
        return_type = node.children[2].leaf

        # adiciona símbolo da função
        self.symtab.add_symbol(func_id, type=return_type, kind='function')

        # entra no novo escopo
        self.symtab.enter_scope(func_id)

        # adiciona parâmetros ao escopo da função
        for param in param_list.children:
            ids, type_node = param.children
            for id_node in ids.children:
                self.symtab.add_symbol(id_node.leaf, type=type_node.leaf, kind='parameter')

        # analisa o corpo da função
        self._analyze_node(node.children[3])

        self.symtab.exit_scope()


    def _analyze_compound(self, node):
        return self._analyze_node(node.children[0])

    def _analyze_statement_list(self, node):
        for stmt in node.children:
            self._analyze_node(stmt)

    def _analyze_assignment(self, node):
        var_node = node.children[0]
        expr_node = node.children[1]
        var_type = self._get_expression_type(var_node)
        expr_type = self._get_expression_type(expr_node)
        if var_type and expr_type and var_type != expr_type:
            self.errors.append(f"Erro de tipo: não pode atribuir '{expr_type}' a '{var_type}'")

    def _analyze_if(self, node):
        cond_type = self._get_expression_type(node.children[0])
        if cond_type != 'boolean':
            self.errors.append("Erro: condição do 'if' deve ser booleana")
        self._analyze_node(node.children[1])
        if len(node.children) > 2:
            self._analyze_node(node.children[2])

    def _analyze_while(self, node):
        cond_type = self._get_expression_type(node.children[0])
        if cond_type != 'boolean':
            self.errors.append("Erro: condição do 'while' deve ser booleana")
        self._analyze_node(node.children[1])

    def _analyze_for(self, node):
        self._analyze_node(node.children[1])  # valor inicial
        self._analyze_node(node.children[2])  # valor final
        self._analyze_node(node.children[3])  # corpo

    def _analyze_procedure_call(self, node):
        proc_name = node.children[0].leaf
        symbol = self.symtab.lookup(proc_name)
        if not symbol:
            self.errors.append(f"Erro: procedimento '{proc_name}' não declarado")

    def _analyze_writeln(self, node):
        if node.children:
            self._analyze_node(node.children[0])
            
    def _analyze_write(self, node): # NOVO 
        if node.children:
            self._analyze_node(node.children[0])

    def _analyze_readln(self, node):
        for var_node in node.children:
            if self.symtab.lookup(var_node.leaf) is None:
                self.errors.append(f"Erro: variável '{var_node.leaf}' não declarada")
    
    def _analyze_binary_op(self, node):
        left_type = self._get_expression_type(node.children[0])
        right_type = self._get_expression_type(node.children[1])
        op = node.leaf.lower()

        if op in ['=', '<>', '<', '>', '<=', '>=']:
            if left_type != right_type:
                self.errors.append("Erro: comparação entre tipos diferentes")
            return 'boolean'

        elif op in ['and', 'or']:
            if left_type != 'boolean' or right_type != 'boolean':
                self.errors.append("Erro: operador lógico com operandos não booleanos")
            return 'boolean'

        elif op in ['+', '-', '*', 'div', 'mod', '/']:
            if op in ['div', 'mod']:
                if left_type != 'integer' or right_type != 'integer':
                    self.errors.append("Erro: operação 'div' ou 'mod' requer operandos do tipo inteiro")
                return 'integer'
            elif op == '/':
                if left_type not in ['integer', 'real'] or right_type not in ['integer', 'real']:
                    self.errors.append("Erro: operação '/' requer operandos do tipo inteiro ou real")
                #return 'real'  # <--- Força o tipo real ?????? 
                if left_type == 'real' or right_type == 'real':
                        return 'real'
                else:
                        return 'integer'
            else:
                if left_type not in ['integer', 'real'] or right_type not in ['integer', 'real']:
                    self.errors.append("Erro: operação aritmética requer operandos do tipo inteiro ou real")
                if left_type == 'real' or right_type == 'real':
                    return 'real'
                else:
                    return 'integer'
        else:
            self.errors.append(f"Erro: operador binário desconhecido '{op}'")
            return None

    def _analyze_unary_op(self, node):
        return self._get_expression_type(node.children[0])

    def _get_expression_type(self, node):
        if node is None:
            return None
        if node.type == 'integer':
            return 'integer'
        elif node.type == 'real':
            return 'real'
        elif node.type == 'formatted_output': 
            return self._get_expression_type(node.children[0])
        elif node.type == 'boolean':
            return 'boolean'
        elif node.type == 'string':
            return 'string'
        elif node.type == 'variable':
            symbol = self.symtab.lookup(node.leaf)
            if symbol:
                return symbol.type
            else:
                self.errors.append(f"Erro: variável '{node.leaf}' não declarada")
                return None
            
        elif node.type == 'array_access':
            array_name = node.leaf
            array_info = self.symtab.lookup(array_name) 
            if array_info is None:
                self.errors.append(f"Erro: variável '{array_name}' não declarada")
                return None

            # Verifica se o array foi corretamente identificado
            if not hasattr(array_info, "element_type") or array_info.element_type is None:
                self.errors.append(f"Erro: '{array_name}' não é um array")
                return None

            # Verificar se índice é inteiro
            index_type = self._get_expression_type(node.children[0])
            if index_type != 'integer':
                self.errors.append(f"Erro: índice do array '{array_name}' deve ser inteiro")
            return array_info.element_type  

        elif node.type in ['binary_op', 'unary_op']:
            return self._analyze_node(node)
        return None