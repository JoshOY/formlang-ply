from .base_parser import BaseParser

reserved = {
    'Text': 'TEXT',
    'ShortInput': 'SHORT_INPUT',
    'LongInput': 'LONG_INPUT',
    'SingleChoice': 'SINGLE_CHOICE',
    'MultipleChoice': 'MULTIPLE_CHOICE',
    'Select': 'SELECT',
    'DatePicker': 'DATE_PICKER',
    'required': 'REQUIRED',
    # 'trigger': 'TRIGGER',
}


# noinspection PyMethodMayBeStatic
class FormLangASTParser(BaseParser):
    tokens = [
        "EQ",
        "STRING",
        "MARKDOWN_STRING",
        "LPAREN",
        "RPAREN",
        "LBRACE",
        "RBRACE",
        "NUMBER",
        "NEWLINE",
        "ID",
    ] + list(reserved.values())

    t_ignore = ' \t'

    def t_EQ(self, t):
        r'\='
        t.value = ('EQ', '=')
        return t

    def t_LPAREN(self, t):
        r'\('
        t.value = ('LPAREN', '(')
        return t

    def t_RPAREN(self, t):
        r'\)'
        t.value = ('RPAREN', ')')
        return t

    def t_LBRACE(self, t):
        r'\{'
        t.value = ('LBRACE', '{')
        return t

    def t_RBRACE(self, t):
        r'\}'
        t.value = ('RBRACE', '}')
        return t

    def t_STRING(self, t):
        r'\"(?:[^\"]|\.)*\"'
        t.value = t.value.strip()
        t.value = ('STRING', t.value)
        return t

    def t_MARKDOWN_STRING(self, t):
        r'```(?:[^\\"]|\\.)*```'
        t.value = t.value.strip()
        t.value = ('MARKDOWN_STRING', t.value)
        return t

    def t_NUMBER(self, t):
        r'\d+'
        t.value = int(t.value)
        t.value = ('NUMBER', t.value)
        return t

    def t_ID(self, t):
        r'[a-zA-Z_][a-zA-Z_0-9]*'
        t.type = reserved.get(t.value, 'ID')  # Check for reserved words
        t.value = ('ID', t.value)
        return t

    def t_NEWLINE(self, t):
        r'((?:\n)|(?:\r\n))+'
        t.lexer.lineno += t.value.count("\n")
        t.value = ('NEWLINE', t.value)
        return t

    def t_error(self, t):
        print("Illegal character '%s'" % t.value[0])
        t.lexer.skip(1)

    # =========================================
    # Yacc part
    # =========================================
    # Precedence rules for the arithmetic operators
    precedence = ()

    def p_programme(self, p):
        """programme : empty
                     | NEWLINE
                     | form
                     | form NEWLINE"""
        if p[1] is not None:
            p[0] = ('Programme', p[1])
        else:
            p[0] = ('Programme',)

    def p_form(self, p):
        """form : question
                | required_question
                | question_complex
                | required_question_complex
                | form NEWLINE question
                | form NEWLINE question_complex
                | form NEWLINE required_question
                | form NEWLINE required_question_complex"""
        if len(p) == 2:
            p[0] = ('form', p[1])
        elif len(p) == 4:
            if not p[1]:
                p[1] = ('form',)
            p[0] = p[1] + (p[3],)
        print("DEBUG in p_form; p[0] =", p[0])

    def p_question_type(self, p):
        """question_type : TEXT
                         | SHORT_INPUT
                         | LONG_INPUT
                         | SINGLE_CHOICE
                         | MULTIPLE_CHOICE
                         | SELECT
                         | DATE_PICKER"""
        p[0] = ('question_type', p[1])

    def p_question(self, p):
        """question : question_type LPAREN STRING RPAREN
                    | question_type LPAREN MARKDOWN_STRING RPAREN
                    | question_type LPAREN NEWLINE STRING RPAREN
                    | question_type LPAREN STRING NEWLINE RPAREN
                    | question_type LPAREN NEWLINE STRING NEWLINE RPAREN
                    | question_type LPAREN NEWLINE MARKDOWN_STRING RPAREN
                    | question_type LPAREN MARKDOWN_STRING NEWLINE RPAREN
                    | question_type LPAREN NEWLINE MARKDOWN_STRING NEWLINE RPAREN"""
        if len(p) == 5:
            p[0] = ('question', p[3])
        elif p[3][0] != 'NEWLINE':
            p[0] = ('question', p[4])
        else:
            p[0] = ('question', p[3])

    def p_block_start(self, p):
        """block_start : LBRACE
                       | NEWLINE LBRACE
                       | LBRACE NEWLINE
                       | NEWLINE LBRACE NEWLINE
        """
        p[0] = ('block_start',)

    def p_block_end(self, p):
        """block_end : RBRACE
                     | NEWLINE RBRACE
        """
        p[0] = ('block_end',)

    def p_question_complex(self, p):
        """question_complex : question_type block_start block_end
                    | question_type block_start question_body block_end"""
        if len(p) == 4:
            p[0] = ('question_complex', p[1],)
        else:
            p[0] = ('question_complex', p[1], p[3],)

    def p_question_body(self, p):
        """question_body : question_property_definition
                         | question_option_definition
                         | question_body NEWLINE question_property_definition
                         | question_body NEWLINE question_option_definition"""
        if len(p) == 2:
            p[0] = ('question_body', p[1])
        else:
            p[0] = p[1] + (p[3],)

    def p_question_property_definition(self, p):
        """question_property_definition : ID EQ STRING
                                | ID EQ MARKDOWN_STRING
                                | ID EQ NUMBER"""
        p[0] = ('question_property_definition', p[1], p[2], p[3])

    def p_question_option_definition(self, p):
        """question_option_definition : NUMBER EQ STRING
                                      | NUMBER EQ MARKDOWN_STRING"""
        p[0] = ('question_option_definition', p[1], p[2], p[3])

    def p_required_question(self, p):
        """required_question : REQUIRED question"""
        p[0] = ('required', p[2])

    def p_required_question_complex(self, p):
        """required_question_complex : REQUIRED question_complex"""
        p[0] = ('required', p[2])

    def p_empty(self, p):
        """empty : """
        pass

    # Error rule for syntax errors
    def p_error(self, p):
        print("--- Syntax error! ---")
        print(p)
