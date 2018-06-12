from aiohttp import web
from .routes import app_routes
from .controllers import *
from .utils.path_resolver import PathResolver

@app_routes.get('/')
async def hello_handler(request):
    return web.Response(text="Hello world!")

def run():
    app = web.Application()

    # set up static file directory
    static_path = PathResolver.resolve_by_root('app/static')
    app.router.add_static('/public', static_path)

    app.add_routes(app_routes)
    web.run_app(app)
