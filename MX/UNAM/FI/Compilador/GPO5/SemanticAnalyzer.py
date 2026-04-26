from rply import LexerGenerator
from Tree import Arbol

class SemAnalyzer():

    def __init__(self, sym_table):
        self.lexer = LexerGenerator()
        # Symbol Table
        self.sym_table = sym_table

        self.num_errors = 0

    def verify(self, ast):
        match ast.etiqueta():
            case "program":
                # We perform a semantic verification of each instruction in the program body
                for instruction in ast.hijos():
                    self.verifySubTree(instruction)
            case _:
                print("Error: The AST root is not an instance of 'program'")
                self.num_errors += 1
        return self.num_errors

    def verifySubTree(self, ast):

        if isinstance(ast, list):
            for child in ast:
                self.verifySubTree(child)
            return
        if not hasattr(ast, 'hijos') and isinstance(ast, ('real', 'int', 'string', 'bool')):
            return

        elif hasattr(ast, 'hijos'):
            hijos = ast.hijos()

            match ast.etiqueta():  # Semantic analysis depends on the node type

                case "=":

                    if len(hijos) == 2:
                        if hijos[0] in self.sym_table:

                            if self.tipoSubTree(hijos[1]) != self.tipoSubTree(hijos[0]) and self.tipoSubTree(
                                    hijos[0]) != None:

                                print("**SEMANTIC ERROR: Expected a " + str(
                                    self.tipoSubTree(hijos[0])) + " value for the variable " + str(hijos[0]))
                                self.num_errors += 1
                                return None
                            elif self.tipoSubTree(hijos[1]) == self.tipoSubTree(hijos[0]):
                                return None
                            else:
                                print("**SEMANTIC ERROR: The variable " + str(hijos[0]) + " has not been declared yet")
                                self.num_errors += 1
                                return None
                        else:
                            print("**SEMANTIC ERROR: The variable " + str(hijos[0]) + " has not been declared yet")
                            self.num_errors += 1
                            return None
                case 'if':
                    if self.tipoSubTree(hijos[0]) != 'bool':
                        print("**SEMANTIC ERROR: Expected a 'bool' value for the 'if' condition")
                        self.num_errors += 1
                        return None
                    for instruction in hijos[1].hijos():
                        self.verifySubTree(instruction)
                case 'if-else':
                    if self.tipoSubTree(hijos[0]) != 'bool':
                        print("**SEMANTIC ERROR: Expected a 'bool' value for the 'if' condition")
                        self.num_errors += 1
                        return None
                    for instruction in hijos[1].hijos():
                        self.verifySubTree(instruction)
                    for instruction in hijos[2].hijos():
                        self.verifySubTree(instruction)
                case 'while':
                    for instruction in hijos[1:]:
                        self.verifySubTree(instruction)
                    if self.tipoSubTree(hijos[0]) != 'bool':
                        print("**SEMANTIC ERROR: Expected a 'bool' value for the 'while' condition")
                        self.num_errors += 1
                        return None

                case 'for':
                    if self.tipoSubTree(hijos[0]) != 'int' or self.tipoSubTree(
                            hijos[1]) != 'int' or self.tipoSubTree(hijos[2]) != 'int':
                        print("**SEMANTIC ERROR: Expected an 'int' value for the counter " + str(hijos[0]))
                        self.num_errors += 1
                        return None
                    for instruction in hijos[3:]:
                        self.verifySubTree(instruction)
                case 'write':
                    if self.tipoSubTree(hijos[0]) == None:
                        print("**SEMANTIC ERROR: Cannot apply 'write' to a null expression")
                        self.num_errors += 1
                        return None

                case "string":
                    if len(hijos) == 2:
                        if "string" != self.tipoSubTree(hijos[1]):
                            print("**SEMANTIC ERROR: Expected a 'string' value for the variable " + str(hijos[0]))
                            self.num_errors += 1
                            return None
                case "real":
                    if len(hijos) == 2:
                        if "real" != self.tipoSubTree(hijos[1]):
                            print("**SEMANTIC ERROR: Expected a 'real' value for the variable " + str(hijos[0]))
                            self.num_errors += 1
                            return None
                case "int":
                    if len(hijos) == 2:
                        if "int" != self.tipoSubTree(hijos[1]):
                            print("**SEMANTIC ERROR: Expected an 'int' value for the variable " + str(hijos[0]))
                            self.num_errors += 1
                            return None
                case "bool":
                    if len(hijos) == 2:
                        if "bool" != self.tipoSubTree(hijos[1]):
                            print("**SEMANTIC ERROR: Expected a 'bool' value for the variable " + str(hijos[0]))
                            self.num_errors += 1
                            return None
                case 'or' | 'and':

                    if self.tipoSubTree(hijos[0]) != 'bool' or self.tipoSubTree(hijos[1]) != 'bool':
                        return None

                case 'not':
                    if self.tipoSubTree(hijos[0]) != 'bool':
                        print("**SEMANTIC ERROR: Expected a 'bool' value for the 'not' operator")
                        self.num_errors += 1
                        return None
                case 'read':
                    tipo = self.tipoSubTree(hijos[0])
                    if tipo is None:
                        print(f"**SEMANTIC ERROR: The variable {hijos[0]} has not been declared yet")
                        self.num_errors += 1
                        return None
                    elif tipo not in ['string', 'int', 'real', 'bool']:
                        print(f"**SEMANTIC ERROR: Cannot apply 'read' to a variable of type {tipo}")
                        self.num_errors += 1
                        return None
                case _:
                    return
        else:
            return

    # Function to calculate the type of a value
    # Examples:
    # "hello" -> string

    def tipoSubTree(self, ast):

        if isinstance(ast, Arbol) and ast.etiqueta() == "bool_literal":
            return "bool"
        if isinstance(ast, str) and ast in self.sym_table and self.sym_table[ast]['tipo'] != None:
            return self.sym_table[ast]['tipo']
        elif isinstance(ast, str) and ast in self.sym_table and self.sym_table[ast]['tipo'] == None:

            return None
        for key, data in self.sym_table.items():
            if data.get('valor') == str(ast):
                varname = key
                tipopre = data['tipo']
                if tipopre == 'int':
                    try:
                        return 'int'
                    except ValueError:
                        print("**SEMANTIC ERROR: Expected an integer value for the variable " + str(varname))
                        self.num_errors += 1
                        return None
                if tipopre == 'real':
                    try:
                        return 'real'
                    except ValueError:
                        print("**SEMANTIC ERROR: Expected a 'real' value for the variable " + str(varname))
                        self.num_errors += 1
                        return None

        if isinstance(ast, str):
            try:
                int(ast)
                return 'int'
            except ValueError:
                pass
            try:
                float(ast)
                return 'real'
            except ValueError:
                pass
            if ast == 'True' or ast == 'False':
                return 'bool'
            return "string"

        if isinstance(ast, int):
            return "int"
        if isinstance(ast, float):
            return "real"
        if isinstance(ast, bool):
            return "bool"

        if hasattr(ast, 'hijos') and ast.hijos():
            hijos = ast.hijos()
        # Here would go the type calculation for arithmetic-logical operators
        match ast.etiqueta():

            case "+" | "-":

                if self.tipoSubTree(hijos[0]) != self.tipoSubTree(hijos[1]):

                    if self.tipoSubTree(hijos[0]) in ("int", "real"):
                        print("**SEMANTIC ERROR: Expected 2 " + str(self.tipoSubTree(
                            hijos[0])) + " values for the operator " + str(ast.etiqueta()))

                    else:
                        print("**SEMANTIC ERROR: Expected numeric values for the operator " + ast.etiqueta())
                    self.num_errors += 1
                    return None
                elif self.tipoSubTree(hijos[0]) == "int":
                    return "int"
                elif self.tipoSubTree(hijos[0]) == "real":
                    return "real"
                else:
                    print("**SEMANTIC ERROR: Expected numeric values for the operator " + ast.etiqueta())
                    self.num_errors += 1
                    return None

            case "*" | "/":

                if (self.tipoSubTree(hijos[0])) in ('int', 'real') and self.tipoSubTree(hijos[1]) in ("int",
                                                                                                         "real"):
                    if self.tipoSubTree(hijos[0]) == 'int' and self.tipoSubTree(
                            hijos[1]) == 'int' and ast.etiqueta() != '/':
                        return 'int'
                    return 'real'
                else:
                    print("**SEMANTIC ERROR: Expected numeric values for the operator " + ast.etiqueta())
                    self.num_errors += 1
                    return None

            case "==" | "!=":
                tipo1 = self.tipoSubTree(hijos[0])
                tipo2 = self.tipoSubTree(hijos[1])
                if tipo1 != tipo2:
                    if tipo1 in ("int", "real") and tipo2 in ("int", "real"):
                        return 'bool'
                    print(f'**SEMANTIC ERROR: Expected a {tipo1} value for the operand {str(hijos[0])}')
                    self.num_errors += 1
                    return 'bool'
                else:
                    return 'bool'
            case '<' | '>' | '<=' | '>=':

                if self.tipoSubTree(hijos[0]) != self.tipoSubTree(hijos[1]):

                    if self.tipoSubTree(hijos[0]) in ("int", "real"):
                        print("**SEMANTIC ERROR: Expected a " + str(self.tipoSubTree(
                            hijos[0])) + " value for the operand " + str(hijos[0]))

                    else:
                        print("**SEMANTIC ERROR: Expected numeric values for the operator " + ast.etiqueta())
                    self.num_errors += 1
                    return 'bool'

                if self.tipoSubTree(hijos[0]) in ("int", 'real'):
                    return "bool"
                else:
                    print("**SEMANTIC ERROR: Expected numeric values for the operator " + ast.etiqueta())
                    self.num_errors += 1
                    return 'bool'

            case 'or' | 'and':

                if self.tipoSubTree(hijos[0]) != 'bool' or self.tipoSubTree(hijos[1]) != 'bool':
                    print("**SEMANTIC ERROR: Expected a 'bool' value for the operator " + ast.etiqueta())
                    self.num_errors += 1
                    return None
                return 'bool'
            case 'not':
                if self.tipoSubTree(hijos[0]) != 'bool':
                    print("**SEMANTIC ERROR: Expected a 'bool' value for the 'not' operator")
                    self.num_errors += 1
                    return None
                return 'bool'
            case _:
                # If the node has children, we evaluate them
                hijos = ast.hijos()
                if hijos:
                    for hijo in hijos:
                        self.tipoSubTree(hijo)
                else:
                    return None