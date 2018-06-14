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

@app_routes.post('/api/ast_generate')
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
    ast_parser.restart()
    return web.json_response({
        'ok': True,
        'result': transform_structure(result),
    })
