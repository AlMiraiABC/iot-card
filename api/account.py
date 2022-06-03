from aiohttp import web
from aiohttp.web_exceptions import HTTPMethodNotAllowed
from aiohttp.web_request import Request
from services.account_service import AccountService

from api.constants import json_response
from api.middlewares import (ACCOUNT_STORAGE, base_exception_middleware,
                             login_middleware)

app = web.Application(
    middlewares=[base_exception_middleware, login_middleware])
routes = web.RouteTableDef()


def _get_account(request: Request) -> AccountService:
    return request[ACCOUNT_STORAGE]


@routes.get('/')
async def manage(request: Request):
    """Get current loged in account informations."""
    email = _get_account(request).email
    account = AccountService(email).config
    return json_response(data=account)


@routes.post('/modify')
async def modify(request: Request):
    """Modify current account informations."""
    raise HTTPMethodNotAllowed('Not implemented.')


@routes.post('/delete')
async def delete(request: Request):
    """Delete current account."""
    raise HTTPMethodNotAllowed('Not implemented.')

app.add_routes(routes)
