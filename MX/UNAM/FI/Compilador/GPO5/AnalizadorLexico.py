from rply import LexerGenerator



class Lexer():

    def __init__(self):
        self.lexer = LexerGenerator()

    def _add_tokens(self):
        # LEXEMS/TOKENS
        # SYNTAX:
        # self.lexer.add('TOKEN_NAME', r'REGEX_TO_IDENTIFY_IT_BY')
        self.lexer.add('START', r'Start')
        self.lexer.add('L_BRACKET', r'\{')
        self.lexer.add('R_BRACKET', r'\}')
        self.lexer.add('L_PARENTHESYS', r'\(')
        self.lexer.add('R_PARENTHESYS', r'\)')
        self.lexer.add('SEMI_COLON', r'\;')


        self.lexer.add('IF', r'if')
        self.lexer.add('THEN', r'then')
        self.lexer.add('ELSE', r'else')
        self.lexer.add('WHILE', r'while')
        self.lexer.add('FOR', r'for')
        self.lexer.add('FROM', r'from')
        self.lexer.add('TO', r'to')



        self.lexer.add('REAL_NUMBER', r'-?\d+\.\d+')
        self.lexer.add('INTEGER', r'-?\d+')
        self.lexer.add('STRING', r'".*"')
        self.lexer.add('BOOL', r'True|False')

        # --- Operators ---
        self.lexer.add('ARIT_OP', r'\+|-|\*|/')
        self.lexer.add('COMP_OP', r'==|!=|>=|<=|<|>')
        self.lexer.add('BOOL_OP', r'\b(or|and|not)\b')
        self.lexer.add('ASIG_OP', r'=')

        # --- I/O Operations ---
        self.lexer.add('READ_OP', r'read')
        self.lexer.add('WRITING_OP', r'printf')

        # --- Identifiers ---
        self.lexer.add('TYPE', r'int|bool|string|real')
        self.lexer.add('ID', r'[a-z][a-zA-Z_\d]*')

        self.lexer.add('COMMENT', r'#.*')

        # --- Whitespace and Comments ---
        self.lexer.ignore(r'\s+')
        
    def get_lexer(self):
        self._add_tokens()
        return self.lexer.build()
