from formlang.parser import FormLangParser

if __name__ == '__main__':
    with open('./form_input.formlang', 'r') as test_input_file:
        input_program = test_input_file.read()
    parser = FormLangParser()
    parser.input(input_program)
