class CodeGenerator:
    def __init__(self, symtab):
        self.symtab = symtab
        self.code = []
        self.temp_counter = 0
        self.label_counter = 0
        self.current_offset = 0
        self.counter = 0
        self.var_declarations = []
        self.main_code = []
        self.errors = []

    def emit(self, instruction):
        self.main_code.append(instruction)

    def generate(self, ast):
        if ast is None:
            return []

        self.code = []
        self.var_declarations = []
        self.main_code = []
        self._generate_code(ast)

        # concatena declarações + start + código + stop
        full_code = []
        full_code += self.var_declarations
        full_code.append("start")
        full_code += self.main_code
        full_code.append("stop")

        return full_code

    def _generate_code(self, node):
        if node is None:
            return

        method = getattr(self, f"_generate_{node.type}", None)
        if method:
            method(node)
        else:
            for child in node.children:
                self._generate_code(child)

    def _generate_program(self, node):
        self._generate_code(node.children[0])

    def _generate_block(self, node):
        for child in node.children:
            self._generate_code(child)

    def _generate_declarations(self, node):
        for child in node.children:
            self._generate_code(child)

    def _generate_var_declarations(self, node):
        for child in node.children:
            self._generate_code(child)
            
    def _generate_halt(self, node):
        self.emit("stop")

    def _generate_var_declaration(self, node):
        ids_node, type_node = node.children
        var_type = type_node.leaf if type_node.leaf else type_node.type  # handles 'integer', 'array', etc.

        for id_node in ids_node.children:
            var_name = id_node.leaf
            symbol = self.symtab.lookup(var_name)

            if symbol:
                if symbol.address is None:
                    symbol.address = self.current_offset

                    if symbol.type == "array":
                        self.var_declarations.append(f"pushi {symbol.size}")    # total size
                        self.var_declarations.append("allocn")                  # allocate on heap
                        self.var_declarations.append(f"storeg {symbol.address}")  # store pointer in gp

                        for i in range(symbol.size):
                            self.var_declarations.append(f"pushst {symbol.address}")
                            self.var_declarations.append(f"pushi 0")
                            self.var_declarations.append(f"store {i}")

                        self.current_offset += 1  # only one global slot is needed (for pointer)
                    else:
                        # Scalar variable
                        self.var_declarations.append("pushi 0")
                        self.var_declarations.append(f"storeg {symbol.address}")
                        self.current_offset += 1

    def _generate_statement_list(self, node):
        for stmt in node.children:
            self._generate_code(stmt)

    def _generate_assignment(self, node):
        var_node = node.children[0]
        expr_node = node.children[1]

        self._generate_code(expr_node)

        if var_node.type == 'variable':
            symbol = self.symtab.lookup(var_node.leaf)
            self.emit(f"storeg {symbol.address}")

    def _generate_variable(self, node):
        symbol = self.symtab.lookup(node.leaf)
        
        # Verificar se estamos em um contexto após loadn
        # Poderíamos adicionar um flag para rastrear isso
        if hasattr(self, '_after_loadn') and self._after_loadn:
            # Se estamos após um loadn, não precisamos do pushg adicional
            self._after_loadn = False  # Resetar a flag
            return
            
        self.emit(f"pushg {symbol.address}")  


    def _generate_integer(self, node):
        self.emit(f"pushi {node.leaf}")
        
    def _generate_real(self, node):
        self.emit(f"pushf {node.leaf}")

    def _generate_string(self, node):
        self.emit(f"pushs \"{node.leaf}\"")

    def _generate_boolean(self, node):
        self.emit(f"pushi {1 if node.leaf == 'true' else 0}")

    def _generate_binary_op(self, node):
        self._generate_code(node.children[0])
        self._generate_code(node.children[1])
        op = node.leaf
        if op == '+':
            self.emit("add")
        elif op == '-':
            self.emit("sub")
        elif op == '*':
            self.emit("mul")
        elif op == 'div':
            self.emit("div")
        elif op == '/':
            self.emit("fdiv")
        elif op == 'mod':
            self.emit("mod")
        elif op == '=':
            self.emit("equal")
        elif op == '<':
            self.emit("inf")
        elif op == '<=':
            self.emit("infeq")
        elif op == '>':
            self.emit("sup")
        elif op == '>=':
            self.emit("supeq")
        elif op == '<>':
            self.emit("equal")
            self.emit("not")
        elif op == 'and':
            self.emit("and")
        elif op == 'or':
            self.emit("or")

    def _generate_unary_op(self, node):
        self._generate_code(node.children[0])
        if node.leaf == 'not':
            self.emit("not")
        elif node.leaf == '-':
            self.emit("pushi -1")
            self.emit("mul")

    def _generate_if(self, node):
        false_label = self._new_label("ELSE")
        end_label = self._new_label("ENDIF")
        self._generate_code(node.children[0])
        self.emit(f"jz {false_label}")
        self._generate_code(node.children[1])
        self.emit(f"jump {end_label}")
        self.emit(f"{false_label}:")
        if len(node.children) > 2:
            self._generate_code(node.children[2])
        self.emit(f"{end_label}:")

    def _generate_while(self, node):
        start_label = self._new_label("WHILE")
        end_label = self._new_label("ENDWHILE")

        self.emit(f"{start_label}:")
        self._generate_code(node.children[0])
        self.emit(f"jz {end_label}")
        self._generate_code(node.children[1])
        self.emit(f"jump {start_label}")
        self.emit(f"{end_label}:")


    def _generate_for(self, node):
        var_node = node.children[0]
        var_name = var_node.leaf
        direction = node.leaf  # "to" ou "downto"
        symbol = self.symtab.lookup(var_name)
        if not symbol:
            self.errors.append(f"Erro: variável '{var_name}' não declarada")
            return

        self.counter = symbol.address
        end_label = self._new_label("ENDFOR")
        start_label = self._new_label("FOR")

        # Valor inicial
        self._generate_code(node.children[1])
        self.emit(f"storeg {symbol.address}")

        # Reserva memória e guarda valor final
        final_var = self.current_offset
        self.current_offset += 1
        self.var_declarations.append(f"pushi 0")
        self.var_declarations.append(f"storeg {final_var}")
        self._generate_code(node.children[2])
        self.emit(f"storeg {final_var}")
        self.emit(f"{start_label}:")
        self.emit(f"pushg {symbol.address}")
        self.emit(f"pushg {final_var}")
        self.emit("sup" if direction == "to" else "inf")
        self.emit("not")  # Inverte a condição
        self.emit(f"jz {end_label}")
        self._generate_code(node.children[3])
        self.emit(f"pushg {symbol.address}")
        self.emit(f"pushi {-1 if direction == 'downto' else 1}")
        self.emit("add")
        self.emit(f"storeg {symbol.address}")
        self.emit(f"jump {start_label}")
        self.emit(f"{end_label}:")

    def _generate_writeln(self, node):
        if node.children:
            for expr in node.children[0].children:
                if expr.type == 'formatted_output':
                    self._generate_code(expr)  # já inclui writef ou writei
                else:
                    self._generate_code(expr)
                    if expr.type == 'string':
                        self.emit("writes")
                    elif expr.type == 'real':
                        self.emit("writef")  # ← opcional se tiveres float direto
                    else:
                        self.emit("writei")
        self.emit("writeln")
        
    def _generate_write(self, node):
        if node.children:
            for expr in node.children[0].children:
                if expr.type == 'formatted_output':
                    self._generate_code(expr)  # já inclui writef ou writei
                else:
                    self._generate_code(expr)
                    if expr.type == 'string':
                        self.emit("writes")
                    elif expr.type == 'real':
                        self.emit("writef")  # ← opcional se tiveres float direto
                    else:
                        self.emit("writei")

    def _generate_readln(self, node):
        for var_node in node.children:
            if var_node.type == 'variable':
                symbol = self.symtab.lookup(var_node.leaf)
                self.emit("read")
                if symbol.type == 'real':
                    self.emit("atof")
                else:
                    self.emit("atoi")
                self.emit(f"storeg {symbol.address}")

            elif var_node.type == 'array_access':
                array_name = var_node.leaf
                symbol = self.symtab.lookup(array_name)
                if symbol is None or symbol.type != 'array':
                    print(f"[ERRO] _generate_readln: '{array_name}' não é um array válido")
                    continue

                self.emit(f"pushst {symbol.address}")
                self.emit(f"pushg {self.counter}")
                self.emit(f"pushi 1")
                self.emit("sub")
                self.emit(f"read")
                self.emit(f"atoi")
                self.emit(f"storen")

            else:
                print(f"[ERRO] _generate_readln: tipo inesperado {var_node.type}")

    def _generate_array_access(self, node):
        array_name = node.leaf
        index_expr = node.children[0]

        symbol = self.symtab.lookup(array_name)
        if symbol is None or symbol.type != 'array':
            print(f"[ERRO] _generate_array_access: '{array_name}' não é um array válido")
            return

        # Push the base address (pointer stored in gp[symbol.address])
        self.emit(f"pushst {symbol.address}")
        self.emit(f"pushg {self.counter}")
        self.emit(f"pushi 1")
        self.emit("sub")
        self.emit("loadn")
        self._after_loadn = True
        self._generate_code(index_expr)


    def _new_label(self, base):
        label = f"{base}{self.label_counter}"
        self.label_counter += 1
        return label

