from aiohttp import web
from ..routes import app_routes

@app_routes.get('/demo')
def get_demo(request):
    return web.json_response({
        'ok': True,
    })
