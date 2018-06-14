from aiohttp import web
from ..routes import app_routes
from ..utils.formlang.ast_parser import FormLangASTParser

def transform_structure(ast):
    ret = {}
    if type(ast) == tuple:
        ret["text"] = {
            "name":  ast[0],
        }
        if len(ast) > 1:
            ret["children"] = []
            for n in ast[1:]:
                ret["children"].append(transform_structure(n))
    else:
        ret["text"] = {
            "title": "value",
            "desc":  str(ast),
        }
    return ret

def get_node_type(node):
    return node['text']['name']

def get_node_value(node):
    return node['children'][0]['text']['desc']

def transform_form(node, form=[], parent=None):
    # case Programme
    if get_node_type(node) == 'Programme':
        if 'children' in node:
            transform_form(node['children'][0])
    # case form
    if get_node_type(node) == 'form':
        for n in node['children']:
            transform_form(n)
    # case required
    elif get_node_type(node) == 'required':
        transform_form(node['children'][0])
        form[-1]['isRequired'] = True
    # case question
    elif get_node_type(node) == 'question':
        form.append({})
        type_node = node['children'][0]
        type = type_node['children'][0]['children'][0]['text']['desc']
        # print('Found type =', type)
        form[-1]['type'] = type
        string_node = node['children'][1]
        form[-1]['title'] = string_node['children'][0]['text']['desc']
    # case question_complex
    elif get_node_type(node) == 'question_complex':
        form.append({})
        type_node = node['children'][0]
        type = type_node['children'][0]['children'][0]['text']['desc']
        # print('Found type =', type)
        form[-1]['type'] = type
        body_node = node['children'][1]
        transform_form(body_node)
    # case question_body
    elif get_node_type(node) == 'question_body':
        for def_node in node['children']:
            transform_form(def_node)
    elif get_node_type(node) == 'question_option_definition':
        number = get_node_value(node['children'][0])
        option_text = get_node_value(node['children'][2])
        if 'options' not in form[-1]:
            form[-1]['options'] = {}
        form[-1]['options'][number] = option_text
    elif get_node_type(node) == 'question_property_definition':
        key = get_node_value(node['children'][0])
        val = get_node_value(node['children'][2])
        form[-1][key] = val
    return form


@app_routes.post('/api/form_generate')
async def post_ast_generate(request):
    if request.body_exists:
        body_data = await request.post()
        if 'rawCode' not in body_data:
            return web.HTTPBadRequest()
        raw_code = body_data['rawCode']
        print('------------------')
        print(raw_code)
        print('------------------')
    else:
        return web.HTTPBadRequest()
    ast_parser = FormLangASTParser()
    result = ast_parser.input(raw_code)
    # print(result)
    return web.json_response({
        'ok': True,
        'result': transform_structure(result),
        'form': transform_form(transform_structure(result)),
    })
