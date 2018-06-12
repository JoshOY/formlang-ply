from aiohttp import web
import aiohttp_jinja2
from ..routes import app_routes

@app_routes.view('/')
class IndexView(web.View):
    @aiohttp_jinja2.template('index.jinja2')
    async def get(self):
        pass
