from sanic.response import HTTPResponse
from sanic_oauth import blueprint as oauth_bp


def redirect(to, headers=None, status=302, content_type="text/html; charset=utf-8"):
    headers = headers or {}
    safe_to = to
    headers["Location"] = safe_to
    return HTTPResponse(status=status, headers=headers, content_type=content_type)


oauth_bp.redirect = redirect
