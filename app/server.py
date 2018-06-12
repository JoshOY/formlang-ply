from aiohttp import web
from .routes import app_routes
from .controllers import *
from .utils.path_resolver import PathResolver
import aiohttp_jinja2
import jinja2


def run():
    app = web.Application()

    # setup template rendering engine
    template_path = PathResolver.resolve_by_root('app/templates')
    aiohttp_jinja2.setup(app, loader=jinja2.FileSystemLoader(str(template_path)))

    # set up static file directory
    static_path = PathResolver.resolve_by_root('app/static')
    app.router.add_static('/public', static_path)

    app.add_routes(app_routes)
    web.run_app(app)
