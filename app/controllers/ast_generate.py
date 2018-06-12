from aiohttp import web
from ..routes import app_routes
from ..utils.formlang.ast_parser import FormLangASTParser

@app_routes.post('/api/ast_generate')
async def post_ast_generate(request):
    if request.body_exists:
        body_data = await request.post()
        if 'rawCode' not in body_data:
            return web.HTTPBadRequest()
        raw_code = body_data['rawCode']
    else:
        return web.HTTPBadRequest()
    ast_parser = FormLangASTParser()
    result = ast_parser.input(raw_code)
    print(result)
    return web.json_response({
        'ok': True,
        'result': str(result),
    })
