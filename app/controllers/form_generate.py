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

def get_node_value(node, val_key):
    return node['children'][0]

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
        string_node = node['children'][0]
        form[-1]['title'] = string_node['children'][0]['desc']
    # case question_complex
    elif get_node_type(node) == 'question_complex':
        type_node = node[0]
        body_node = node[1]
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
    print(result)
    return web.json_response({
        'ok': True,
        'result': transform_structure(result),
        'form': transform_form(transform_structure(result)),
    })
