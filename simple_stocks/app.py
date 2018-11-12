import aiohttp
from peewee import SqliteDatabase
from sanic import Sanic
from sanic_jinja2 import SanicJinja2
from sanic_oauth.blueprint import oauth_blueprint
from sanic_session import InMemorySessionInterface, Session

from simple_stocks.config import config


app = Sanic()

app.config.update(config)

app.session_interface = InMemorySessionInterface()

Session(app, interface=app.session_interface)
jinja = SanicJinja2(app, pkg_name="simple_stocks", pkg_path="templates")

app.db = SqliteDatabase(app.config.get("PEEWEE_DATABASE_URI", ":memory:"))

with app.db:
    try:
        from simple_stocks.database.models import User, ApiKey, Portfolio, Transaction

        app.db.create_tables([User, ApiKey, Portfolio, Transaction])
    except Exception:
        pass


def register_bps(sanic_app: Sanic):
    sanic_app.blueprint(oauth_blueprint)

    from simple_stocks.pages.routes import bp as pages_bp

    sanic_app.blueprint(pages_bp, url_prefix="/")


register_bps(app)


@app.listener("before_server_start")
async def init_aiohttp_session(sanic_app: Sanic, _loop):
    sanic_app.async_session = aiohttp.ClientSession()


@app.listener("after_server_stop")
async def close_aiohttp_session(sanic_app: Sanic, _loop):
    await sanic_app.async_session.close()


@app.middleware("request")
async def add_session_to_request(request):
    await request.app.session_interface.open(request)


@app.middleware("response")
async def save_session(request, response):
    await request.app.session_interface.save(request, response)


@app.middleware("request")
async def connect_db(_request):
    app.db.connect()


@app.middleware("response")
async def close_db(_request, _response):
    app.db.close()
