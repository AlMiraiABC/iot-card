from aiohttp import web
from aiohttp.web_request import Request
from services.account_service import AccountService
from services.email_service import EmailService
from api.constants import ErrCode, json_response

from api.middlewares import (ACCOUNT_STORAGE, base_exception_middleware,
                             login_middleware)

app = web.Application(
    middlewares=[base_exception_middleware, login_middleware])
routes = web.RouteTableDef()


def _url_var(request: Request, var: str = 'email', default=None):
    return request.match_info.get(var, default)


def _get_account(request: Request) -> AccountService:
    return request[ACCOUNT_STORAGE]


@routes.post('/send/{card:\d+}')
async def send(request: Request):
    account = _get_account(request)
    receiver = account.config
    card = _url_var(request, 'card')
    ret, ex = await EmailService().send(receiver, card)
    if ret:
        return json_response()
    return json_response(ErrCode.SEND_FAILED, ex)

app.add_routes(routes)
