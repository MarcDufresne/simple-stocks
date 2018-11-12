import logging
from functools import wraps

from aiohttp.web_exceptions import HTTPBadRequest
from peewee import DoesNotExist
from sanic_oauth.core import UserInfo

from simple_stocks.database.models import User
from simple_stocks.monkeypatch import redirect


async def get_registered_user(user_info: UserInfo) -> User:
    try:
        user = User.get(User.email == user_info.email)
    except DoesNotExist:
        user = User.create(email=user_info.email)
    return user


def login_required(get_user=True):
    def decorator(async_handler):
        @wraps(async_handler)
        async def wrapped(request, *_args, **kwargs):

            if request.app.debug and request.headers.get("X-BYPASS-AUTH"):
                user_info = UserInfo(email="test_user@example.com")
                user = await get_registered_user(user_info)
                return await async_handler(request, user, **kwargs)

            if "token" not in request["session"]:
                request["session"]["after_auth_redirect"] = request.path
                return redirect(request.app.config.OAUTH_ENDPOINT_PATH)

            client = request.app.oauth_factory(access_token=request["session"]["token"])

            try:
                user, _info = await client.user_info()
            except (KeyError, HTTPBadRequest) as exc:
                logging.exception(exc)
                return redirect(request.app.config.OAUTH_ENDPOINT_PATH)

            local_email_regex = request.app.config.OAUTH_EMAIL_REGEX

            if local_email_regex and user.email:
                if not local_email_regex.match(user.email):
                    return redirect(request.app.config.OAUTH_ENDPOINT_PATH)

            if get_user:
                user = await get_registered_user(user)
                return await async_handler(request, user, **kwargs)
            return await async_handler(request, **kwargs)

        return wrapped

    return decorator
