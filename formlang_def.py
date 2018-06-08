import ply.lex as lex
import ply.yacc as yacc

with open('./form_input.formlang') as test_input_file:
    input_program = test_input_file.read()

reserved = {
    'Text': 'TEXT',
    'ShortInput': 'SHORT_INPUT',
    'LongInput': 'LONG_INPUT',
    'SingleChoice': 'SINGLE_CHOICE',
    'MultipleChoice': 'MULTIPLE_CHOICE',
    'Select': 'SELECT',
    'DatePicker': 'DATE_PICKER',
    'required': 'REQUIRED',
}

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

# Tokens
t_LPAREN = r'\('
t_RPAREN = r'\)'
t_LBRACE = r'{'
t_RBRACE = r'}'
t_EQ = r'='

def t_STRING(t):
    r'\"(?:[^\"]|\.)*\"'
    t.value = t.value.strip()
    t.value = {
        'type': 'STRING',
        'val': t.value,
    }
    return t

def t_MARKDOWN_STRING(t):
    r'```(?:[^\\"]|\\.)*```'
    t.value = t.value.strip()
    t.value = {
        'type': 'MARKDOWN_STRING',
        'val': t.value,
    }
    return t

def t_NUMBER(t):
    r'\d+'
    t.value = {
        'type': 'NUMBER',
        'val': int(t.value),
    }
    return t

def t_ID(t):
    r'[a-zA-Z_][a-zA-Z_0-9]*'
    t.type = reserved.get(t.value, 'ID')    # Check for reserved words
    return t

def t_NEWLINE(t):
    r'\n+'
    t.lexer.lineno += t.value.count("\n")
    return t

def t_error(t):
    print("Illegal character '%s'" % t.value[0])
    t.lexer.skip(1)


t_ignore = ' \t'


# Build the lexer
lexer = lex.lex()
# Give the lexer some input
lexer.input(input_program)

# Tokenize
while True:
    tok = lexer.token()
    if not tok:
        break      # No more input
    print(tok)

print("=== Start ply.yacc ===")

# Precedence rules for the arithmetic operators
precedence = ()

def p_programme(p):
    """programme : empty
                 | NEWLINE
                 | form
                 | form NEWLINE"""

def p_form(p):
    """form : question
            | required_question
            | form NEWLINE question
            | form NEWLINE required_question"""
    if len(p) == 2:
        p[0] = p[1]
    elif len(p) == 3:
        p[0] = p[1]
    elif len(p) == 4:
        p[0] = (p[1],) + (p[3],)
    print("DEBUG in p_form; p[0] =", p[0])

def p_question_type(p):
    """question_type : TEXT
                     | SHORT_INPUT
                     | LONG_INPUT
                     | SINGLE_CHOICE
                     | MULTIPLE_CHOICE
                     | SELECT
                     | DATE_PICKER"""
    p[0] = p[1]
    print("DEBUG in p_question_type; p[0] =", p[0])

def p_question_body(p):
    """question_body : LBRACE question_body_content RBRACE
                     | LBRACE NEWLINE question_body_content RBRACE
                     | LBRACE question_body_content NEWLINE RBRACE
                     | LBRACE NEWLINE question_body_content NEWLINE RBRACE"""
    p[0] = {
        'node': 'question_body',
    }

def question_body_content(p):
    """question_body_content: empty
                            | ID EQ STRING
                            | ID EQ MARKDOWN_STRING
                            | question_body_content NEWLINE ID EQ STRING
                            | question_body_content NEWLINE ID EQ MARKDOWN_STRING"""
    if len(p) < 3:
        p[0] = {
            'node': 'question_body_content',
            'props': {},
        }

def p_question(p):
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

# TODO!!!
def p_question_complex(p):
    """question : question_type question_body
                | question_type NEWLINE question_body"""
    p[0] = {
        'node': 'question',
    }
    if len(p) == 3:
        p[0]['props'] = p[2]['props']
    else:
        p[0]['props'] = p[3]['props']

def p_required_question(p):
    """required_question : REQUIRED question"""
    p[0] = p[2]
    p[0]['required'] = True

def p_empty(p):
    """empty : """
    pass

# Error rule for syntax errors
def p_error(p):
    print("--- Syntax error! ---")
    print(p)


parser = yacc.yacc(debug=True)
result = parser.parse(input_program)
print(result)
