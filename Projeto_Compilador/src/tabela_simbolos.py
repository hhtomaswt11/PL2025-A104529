class Symbol:
    """
    Classe que representa um símbolo na tabela de símbolos. Um símbolo pode ser uma variável, constante, etc.
    """
    def __init__(self, name, type=None, value=None, kind=None, params=None, scope=None, address=None):
        self.name = name          # nome do símbolo
        self.type = type          # tipo do símbolo (inteiro, real, boolean, etc.)
        self.value = value        # valor para constantes
        self.kind = kind          # tipo de símbolo (variável, função, etc.)
        self.params = params      # parâmetros para functions e procedures
        self.scope = scope        # escopo do símbolo
        self.address = address    # endereço na memória virtual
        self.size = 1             # tamanho do símbolo (para arrays)
        self.dimensions = None    # dimensões para arrays
        self.element_type = None  # tipo dos elementos do array (ex: integer)

    def __repr__(self):
        return f"Symbol(name='{self.name}', type='{self.type}', kind='{self.kind}', scope='{self.scope}')"

class SymbolTable:
    """
    Tabela de símbolos para armazenar informações sobre identificadores no programa. Implementa escopos aninhados.
    """
    def __init__(self):
        # Escopo global
        self.scopes = [{}]
        self.current_scope = 0
        self.scope_names = ["global"]
        
    def enter_scope(self, name):
        """Cria um novo escopo aninhado."""
        self.scopes.append({})
        self.current_scope += 1
        self.scope_names.append(name)
        return self.current_scope
    
    def exit_scope(self):
        """Sai do escopo atual e retorna para o escopo pai."""
        if self.current_scope > 0:
            self.scopes.pop()
            self.scope_names.pop()
            self.current_scope -= 1
        return self.current_scope

    def add_symbol(self, name, type=None, value=None, kind=None, params=None, address=None, size=1, dimensions=None, element_type=None):
        """Adiciona um símbolo na tabela de símbolos, incluindo suporte para arrays."""
        scope_name = self.scope_names[self.current_scope]
        
        # criar um símbolo normal
        symbol = Symbol(name, type, value, kind, params, scope_name, address)
        
        # se for um array, definir as propriedades específicas
        if type == "array":
            symbol.type = "array" 
            symbol.size = size
            symbol.dimensions = dimensions
            symbol.element_type = element_type 

        self.scopes[self.current_scope][name] = symbol
        return symbol

    
    def lookup(self, name, current_scope_only=False):
        """
        Procura um símbolo pelo nome. Começa pelo escopo atual e vai subindo na hierarquia de escopos se não encontrar.
        """
        if current_scope_only:
            if name in self.scopes[self.current_scope]:
                return self.scopes[self.current_scope][name]
            return None
        
        # procura em todos os escopos, começando pelo atual
        for scope_idx in range(self.current_scope, -1, -1):
            if name in self.scopes[scope_idx]:
                return self.scopes[scope_idx][name]
        
        return None
    
    def update_symbol(self, name, **kwargs):
        """Atualiza um símbolo existente."""
        symbol = self.lookup(name)
        if symbol:
            for key, value in kwargs.items():
                if hasattr(symbol, key):
                    setattr(symbol, key, value)
            return symbol
        return None
    
    def get_all_symbols(self):
        """Retorna todos os símbolos de todos os escopos."""
        all_symbols = []
        for scope_idx, scope in enumerate(self.scopes):
            for name, symbol in scope.items():
                all_symbols.append(symbol)
        return all_symbols
