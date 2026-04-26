from rply import ParserGenerator
from nltk.tree import *
from Tree import *

class Parser():

    def __init__(self):
        self.pg = ParserGenerator([
            'START', 'L_BRACKET', 'R_BRACKET',
            'L_PARENTHESYS', 'R_PARENTHESYS', "SEMI_COLON",
            'ARIT_OP', 'COMP_OP', 'WHILE', 'IF', 'ELSE',
            'FOR', 'FROM', 'TO', 'READ_OP', 'WRITING_OP',
            'COMMENT', 'THEN', 'STRING', 'REAL_NUMBER',
            'INTEGER', 'BOOL', 'BOOL_OP', 'TYPE', 'ASIG_OP', 'ID'
        ],
            precedence=[
                ('left', ['BOOL_OP']),
                ('left', ['COMP_OP']),
                ('left', ['ARIT_OP']),
            ])

        self.symbols = {}

    def parse(self):

        @self.pg.production('program : START L_BRACKET instructions R_BRACKET')
        def program(p):
            return Arbol("program", p[2])

        @self.pg.production('instructions : instruction instructions')
        def recursive_instructions(p):
            return [p[0]] + p[1]

        @self.pg.production('instructions : instruction')
        def base_instructions(p):
            return [p[0]]

        @self.pg.production('instruction : writing')
        @self.pg.production('instruction : reading')
        @self.pg.production('instruction : simple_declaration')
        @self.pg.production('instruction : declaration_with_assignment')
        @self.pg.production('instruction : assignment')
        @self.pg.production('instruction : negation_operation')
        @self.pg.production('instruction : if_instruction')
        @self.pg.production('instruction : if_else_instruction')
        @self.pg.production('instruction : while_instruction')
        @self.pg.production('instruction : for_instruction')
        @self.pg.production('instruction : comment')
        def instruction(p):
            return p[0]

        @self.pg.production('writing : WRITING_OP expression SEMI_COLON')
        def writing_exp(p):
            return Arbol("write", [p[1]])

        @self.pg.production('reading : READ_OP ID SEMI_COLON')
        def reading(p):
            return Arbol('read', [p[1].value])

        @self.pg.production('simple_declaration : TYPE ID SEMI_COLON')
        def simple_declaration(p):
            type_val = p[0].value
            name = p[1].value
            self.symbols[name] = {"type": type_val, "value": None}
            return Arbol(type_val, [name])

        @self.pg.production('declaration_with_assignment : TYPE ID ASIG_OP expression SEMI_COLON')
        def declaration_with_assignment(p):
            type_val = p[0].value
            name = p[1].value
            value_val = p[3]
            self.symbols[name] = {"type": type_val, "value": value_val}
            return Arbol(type_val, [name, value_val])

        @self.pg.production('assignment : ID ASIG_OP expression SEMI_COLON')
        def assignment(p):
            name = p[0].value
            value_val = p[2]
            if name not in self.symbols:
                print(f"**WARNING: Variable '{name}' has not been declared. Initialized with None.")
                self.symbols[name] = {"type": None, "value": None}

            self.symbols[name]["value"] = value_val
            return Arbol("=", [name, value_val])

        @self.pg.production('if_instruction : IF expression THEN L_BRACKET instructions R_BRACKET')
        def if_instruction(p):
            return Arbol("if", [p[1], Arbol("then", p[4])])

        @self.pg.production(
            'if_else_instruction : IF expression THEN L_BRACKET instructions R_BRACKET ELSE L_BRACKET instructions R_BRACKET')
        def if_else_instruction(p):
            return Arbol("if-else", [p[1], Arbol("then", p[4]), Arbol("else", p[8])])

        @self.pg.production('while_instruction : WHILE expression L_BRACKET instructions R_BRACKET')
        def while_instruction(p):
            return Arbol("while", [p[1], p[3]])

        @self.pg.production(
            'for_instruction : FOR ID FROM expression TO expression L_BRACKET instructions R_BRACKET')
        def for_instruction(p):
            print("FOR detected with ID:", p[1].value)
            return Arbol("for", [p[1].value, p[3], p[5], p[7]])

        @self.pg.production('comment : COMMENT')
        def comment(p):
            return Arbol("comment", [])

        @self.pg.production('expression : expression ARIT_OP expression')
        def arithmetic_operation(p):
            return Arbol(p[1].value, [p[0], p[2]])

        @self.pg.production('expression : expression COMP_OP expression')
        def comparison_operation(p):
            return Arbol(p[1].value, [p[0], p[2]])

        @self.pg.production('expression : expression BOOL_OP expression')
        def logic_operation(p):
            return Arbol(p[1].value, [p[0], p[2]])

        @self.pg.production('expression : INTEGER')
        def literal_integer(p):
            return p[0].value

        @self.pg.production('expression : REAL_NUMBER')
        def literal_real(p):
            return p[0].value

        @self.pg.production('expression : STRING')
        def literal_string(p):
            return p[0].value

        @self.pg.production('negation_operation : BOOL_OP expression SEMI_COLON')
        def negation_operation(p):
            if p[0].value == "not":
                return Arbol("not", [p[1]])

        @self.pg.production('expression : BOOL')
        def literal_bool(p):
            return Arbol("bool_literal", [p[0].value])

        @self.pg.production("expression : L_PARENTHESYS expression R_PARENTHESYS")
        def expression_parenthesis(p):
            return p[1]

        @self.pg.production("expression : ID")
        def expression_id(p):
            return p[0].value

        @self.pg.error
        def error_handle(token):
            print(">> SYNTAX ERROR at token:", token)
            print("   Line:", token.getsourcepos().lineno, "Column:", token.getsourcepos().colno)
            raise ValueError(token)

    def get_symbols(self):
        return self.symbols

    def get_parser(self):
        return self.pg.build()