from munch import Munch


def configure(config: Munch):
    config.DB_USER = "my_user"
    config.DB_PASSWORD = "qwerty"

    config.OAUTH_CLIENT_ID = "my-client-id.apps.googleusercontent.com"
    config.OAUTH_CLIENT_SECRET = "some-secret"

    config.SECRET_KEY = b"1656a2e2-f25e-4b39-b24f-5ac2aea39cd5"
