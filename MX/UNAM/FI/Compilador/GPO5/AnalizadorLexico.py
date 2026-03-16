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
        # REAL
        self.lexer.add('REAL_NUMBER', r'-?\d+\.\d+')
        # INTEGER
        self.lexer.add('INTEGER', r'-?\d+')
        self.lexer.add('ARIT_OP', r'\+|-|\*|/')
        self.lexer.add('COMP_OP', r'==|!=|>=|<=|<|>')
        # STRING
        self.lexer.add('STRING', r'".*"')
        self.lexer.add('WRITING_OP', r'printf')
        self.lexer.add('COMMENT', r'#.*')

        # BOOLEAN
        self.lexer.add('BOOL', r'Verdadero|Falso')
        self.lexer.add('BOOL_OP', r'\b(or|and|not)\b')

        # IDENTIFIER
        self.lexer.add('TYPE', r'int|bool|string|real')
        self.lexer.add('ASIG_OP', r'=')
        self.lexer.add('ID', r'[a-z][a-zA-Z_\d]*')
        # WHITESPACE AND COMMENTS

        self.lexer.ignore(r'\s+')
        self.lexer.ignore(r'#.*')

    def get_lexer(self):
        self._add_tokens()
        return self.lexer.build()