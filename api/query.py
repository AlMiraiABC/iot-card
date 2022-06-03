import aiohttp
from aiohttp import web
from aiohttp.web_request import Request
from api.constants import json_response
from iot_card.query import Query

app = web.Application()
routes = web.RouteTableDef()


def _url_var(request: Request, var: str = 'card', default=None):
    return request.match_info.get(var, default)


@routes.get('/{card:\d+}/digest')
async def digest(request: Request):
    """Get digest for a card."""
    async with aiohttp.ClientSession() as session:
        query = Query(_url_var(request), session)
        await query.login()
        return json_response(data=await query.get_digest())


@routes.get('/{card:\d+}/account')
async def account(request):
    """Get raw response after login from query."""
    async with aiohttp.ClientSession() as session:
        query = Query(_url_var(request), session)
        await query.login()
        return json_response(data=await query.get_account())


@routes.get('/{card:\d+}/usage')
async def usage(request):
    """Get raw response of data usage from query."""
    async with aiohttp.ClientSession() as session:
        query = Query(_url_var(request), session)
        await query.login()
        return json_response(data=await query.get_usage())

app.add_routes(routes)
