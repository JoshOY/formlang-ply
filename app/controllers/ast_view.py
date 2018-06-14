from aiohttp import web
import aiohttp_jinja2
import json
from ..routes import app_routes

@app_routes.view('/')
class ASTView(web.View):
    @aiohttp_jinja2.template('index.jinja2')
    async def get(self):
        return { 'src_code_init': None }

    @aiohttp_jinja2.template('index.jinja2')
    async def post(self):
        request_body = await self.request.post()
        src_code_init = request_body['srccode']
        return {
            'src_code_init': json.dumps(src_code_init) if src_code_init else None,
        }
