from munch import Munch


def configure(config: Munch):
    config.DB_HOST = "127.0.0.1"
    config.DB_PORT = 5432
    config.DB_USER = "postgres"
    config.DB_PASSWORD = ""
    config.DB_DATABASE = "stocks"

    config.PEEWEE_DATABASE_URI = "app.db"

    config.OAUTH_PROVIDER = "sanic_oauth.providers.GoogleClient"
    config.OAUTH_REDIRECT_URI = ""
    config.OAUTH_SCOPE = "email"
    config.OAUTH_CLIENT_ID = ""
    config.OAUTH_CLIENT_SECRET = ""

    config.REDIS_HOST = "127.0.0.1"
    config.REDIS_PORT = 6379

    config.SECRET_KEY = b""
