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
class FormLangParser(BaseParser):
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

    def t_STRING(self, t):
        r'\"(?:[^\"]|\.)*\"'
        t.value = t.value.strip()
        t.value = {
            'type': 'STRING',
            'val': t.value,
        }
        return t

    def t_MARKDOWN_STRING(self, t):
        r'```(?:[^\\"]|\\.)*```'
        t.value = t.value.strip()
        t.value = {
            'type': 'MARKDOWN_STRING',
            'val': t.value,
        }
        return t

    def t_NUMBER(self, t):
        r'\d+'
        t.value = int(t.value)
        t.value = {
            'type': 'NUMBER',
            'val': t.value,
        }
        return t

    def t_ID(self, t):
        r'[a-zA-Z_][a-zA-Z_0-9]*'
        t.type = reserved.get(t.value, 'ID')  # Check for reserved words
        return t

    def t_NEWLINE(self, t):
        r'\n+'
        t.lexer.lineno += t.value.count("\n")
        return t

    def t_error(self, t):
        print("Illegal character '%s'" % t.value[0])
        t.lexer.skip(1)

    # Precedence rules for the arithmetic operators
    precedence = ()

    def p_programme(self, p):
        """programme : empty
                     | NEWLINE
                     | form
                     | form NEWLINE"""
        if p[1] is not None:
            p[0] = p[1]

    def p_form(self, p):
        """form : question
                | required_question
                | form NEWLINE question
                | form NEWLINE required_question"""
        if len(p) == 2:
            p[0] = [p[1]]
        elif len(p) == 4:
            if not p[1]:
                p[1] = []
            p[0] = p[1]
            p[0].append(p[3])
        print("DEBUG in p_form; p[0] =", p[0])

    def p_question_type(self, p):
        """question_type : TEXT
                         | SHORT_INPUT
                         | LONG_INPUT
                         | SINGLE_CHOICE
                         | MULTIPLE_CHOICE
                         | SELECT
                         | DATE_PICKER"""
        p[0] = p[1]
        print("DEBUG in p_question_type; p[0] =", p[0])

    def p_question_body(self, p):
        """question_body : LBRACE p_question_property_definition RBRACE
                         | LBRACE NEWLINE p_question_property_definition RBRACE
                         | LBRACE p_question_property_definition NEWLINE RBRACE
                         | LBRACE NEWLINE p_question_property_definition NEWLINE RBRACE"""
        if type(p[2]) != str:
            body_content_props = p[2]['props']
        else:
            # print('[!] p[3] =', p[3])
            body_content_props = p[3]['props']
        p[0] = {
            'node': 'question_body',
            'props': body_content_props,
        }

    def p_question_property_definition(self, p):
        """p_question_property_definition : ID EQ STRING
                                | ID EQ MARKDOWN_STRING
                                | ID EQ NUMBER
                                | p_question_property_definition NEWLINE ID EQ STRING
                                | p_question_property_definition NEWLINE ID EQ MARKDOWN_STRING
                                | p_question_property_definition NEWLINE ID EQ NUMBER"""
        if p[0] is None:
            p[0] = {
                'node': 'p_question_property_definition',
                'props': {}
            }
        props = {}
        if len(p) <= 4:
            ID = p[1]
            VAL = p[3]['val']
            props[ID] = VAL
            p[0]['props'][ID] = VAL
        else:
            print('[!] p[1] =', p[1])
            print('[!] p[3] =', p[3])
            print('[!] p[5] =', p[5])
            if p[1] is None:
                p[1] = {
                    'node': 'p_question_property_definition',
                    'props': {}
                }
            else:
                p[0]['props'] = p[1]['props']
            ID = p[3]
            VAL = p[5]['val']
            p[0]['props'][ID] = VAL

    # def p_question_trigger_definition(p):
    #     """
    #     question_trigger_definition : TRIGGER
    #     """

    def p_question(self, p):
        """question : question_type LPAREN STRING RPAREN
                    | question_type LPAREN MARKDOWN_STRING RPAREN
                    | question_type LPAREN NEWLINE STRING RPAREN
                    | question_type LPAREN STRING NEWLINE RPAREN
                    | question_type LPAREN NEWLINE STRING NEWLINE RPAREN
                    | question_type LPAREN NEWLINE MARKDOWN_STRING RPAREN
                    | question_type LPAREN MARKDOWN_STRING NEWLINE RPAREN
                    | question_type LPAREN NEWLINE MARKDOWN_STRING NEWLINE RPAREN"""
        if len(p) <= 5:
            print('DEBUG in p_form_element; p[3] =', p[3])
            p[0] = {
                'node': 'question',
                'props': {
                    'question_type': p[1],
                    'required': False,
                    'title': p[3]['val'],
                    'title_format': p[3]['type'],
                },
            }
        print("DEBUG in p_form_element; p[0] =", p[0])

    def p_question_complex(self, p):
        """question : question_type question_body
                    | question_type NEWLINE question_body"""
        p[0] = {
            'node': 'question',
        }
        if len(p) == 3:
            p[0]['props'] = p[2]['props']
        else:
            p[0]['props'] = p[3]['props']

    def p_required_question(self, p):
        """required_question : REQUIRED question"""
        p[0] = p[2]
        p[0]['props']['required'] = True

    def p_empty(self, p):
        """empty : """
        pass

    # Error rule for syntax errors
    def p_error(self, p):
        print("--- Syntax error! ---")
        print(p)
