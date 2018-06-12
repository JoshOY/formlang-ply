from app.utils.formlang import FormLangParser
from app.utils.formlang.ast_parser import FormLangASTParser

if __name__ == '__main__':
    with open('./form_input.formlang', 'r') as test_input_file:
        input_program = test_input_file.read()
    parser = FormLangParser()
    ast_parser = FormLangASTParser()
    # parser.input(input_program)
    ast_parser.input(input_program)
