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
t_STRING = r'\"(?:[^\"]|\.)*\"'
t_MARKDOWN_STRING = r'```(?:[^\\"]|\\.)*```'
t_LPAREN = r'\('
t_RPAREN = r'\)'
t_LBRACE = r'{'
t_RBRACE = r'}'
t_EQ = r'='

def t_NUMBER(t):
    r'\d+'
    t.value = int(t.value)
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

def p_form(p):
    '''form : form_question
            | form_question NEWLINE form
            | form_question NEWLINE'''
    print("DEBUG in p_form")
    print(p[1])

def p_form_element_type(p):
    '''form_element_type : TEXT
                         | SHORT_INPUT
                         | LONG_INPUT
                         | SINGLE_CHOICE
                         | MULTIPLE_CHOICE
                         | SELECT
                         | DATE_PICKER'''
    p[0] = {}
    p[0]["element_type"] = p[1]
    print("DEBUG in p_form_element_type")
    print(p[0])

def p_form_question_body(p):
    '''
    form_question_body : ID EQ STRING
                       | ID EQ NUMBER
    '''

def p_form_question(p):
    '''
    form_question : form_element_type LPAREN STRING RPAREN
                 | form_element_type LPAREN MARKDOWN_STRING RPAREN
                 | form_element_type LBRACE form_question_body RBRACE
                 | REQUIRED form_question
    '''
    print("DEBUG in p_form_element")
    if (p[2]):
        print(p[1]["element_type"])
    else:
        print('required found')

# Precedence rules for the arithmetic operators
precedence = ()

# Error rule for syntax errors
def p_error(p):
    print("--- Syntax error! ---")
    print(p)


parser = yacc.yacc()
result = parser.parse(input_program)
print(result)

# while True:
#     try:
#         s = input('> ')   # use input() on Python 3
#     except EOFError:
#         break
#     result = parser.parse(s)
#     print(result)
