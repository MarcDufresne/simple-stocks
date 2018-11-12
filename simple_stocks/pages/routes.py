from typing import Dict

from sanic import Blueprint, response
from sanic.request import Request
from sanic.response import redirect

from simple_stocks.app import app, jinja
from simple_stocks.database.models import ApiKey, User
from simple_stocks.utils import login_required


bp = Blueprint("pages")


@bp.route("/")
@jinja.template("home.html")
async def home(_request: Request) -> Dict:
    """
    Home page
    """
    return {}


@bp.route("/register")
@login_required()
async def register(_request: Request, _user: User) -> response.HTTPResponse:
    """
    Registration redirect
    """
    return redirect(app.url_for("pages.portfolios"))


@bp.route("/login")
@login_required()
async def login(_request: Request, _user: User) -> response.HTTPResponse:
    """
    Login redirect
    """
    return redirect(app.url_for("pages.portfolios"))


@bp.route("/portfolios")
@login_required()
async def portfolios(_request: Request, user: User) -> response.HTTPResponse:
    """
    User's list of portfolios
    """
    return response.json({"email": user.email})


@bp.route("/portfolios/<portfolio_id>")
@login_required()
async def portfolio(_request: Request, user: User, portfolio_id: str) -> response.HTTPResponse:
    """
    Details of a specific portfolio
    """
    return response.json({"email": user.email})


@bp.route("/api_keys", methods=["GET"])
@login_required()
async def list_api_keys(_request: Request, user: User) -> response.HTTPResponse:
    api_keys = []
    for api_key in user.api_keys:
        api_keys.append(api_key.to_json())
    return response.json(api_keys)


@bp.route("/api_keys", methods=["POST"])
@login_required()
async def create_api_keys(request: Request, user: User) -> response.HTTPResponse:
    description = request.json.description if request.json else None
    api_key = ApiKey.create(user=user, description=description)
    return response.json(api_key.to_json())
