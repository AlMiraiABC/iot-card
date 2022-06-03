import aiohttp
import aiohttp_jinja2
import jinja2
from aiohttp import web
from aiohttp.web_exceptions import HTTPFound
from aiohttp.web_request import Request
from aiohttp.web_response import Response
from al_utils.logger import Logger

from api.account import app as account_app
from api.constants import ErrCode, json_response
from api.email import app as email_app
from api.middlewares import base_exception_middleware
from api.query import app as query_app
from iot_card.query import Query
from services.account_service import AccountService

logger = Logger(__file__).logger
routes = web.RouteTableDef()


def set_token(service: AccountService, resp: Response):
    token = service.create_token()
    resp = json_response()
    resp.set_cookie('token', token, httponly=True)
    return resp


@routes.get('/{card:\d+}')
@aiohttp_jinja2.template('digest.j2')
async def digest(request: Request):
    """Get card digest."""
    async with aiohttp.ClientSession() as session:
        card = request.match_info.get('card')
        query = Query(card, session)
        await query.login()
        return {'digest': await query.get_digest()}


# @routes.get('/')
# async def root(_):
#     raise HTTPFound('/account.html')


@routes.post('/login')
async def login(request: Request):
    """Log in and redirect to manage page take a token parameter if successfully"""
    data = await request.post()
    email = data.get('email')
    password = data.get('password')
    if not email or not password:
        return json_response(errno=ErrCode.LOGIN_FAILED, msg='Incorrect email or password.')
    try:
        service = AccountService.login(email, password)
        if not service:
            logger.warn(f'Email {email} login failed.')
            return json_response(errno=ErrCode.LOGIN_FAILED,
                                 msg='Incorrect email or password.')
        logger.info(f'Login successfully with {email}.')
        return set_token(service, json_response())
    except Exception as ex:
        logger.warning(f'Occured an exception when login with {email}. {ex}')
        return json_response(errno=ErrCode.LOGIN_FAILED, msg='Incorrect email or password.')


@routes.post('/signup')
async def signup(request: Request):
    data = await request.post()
    email = data.get('email')
    pw = data.get('password')
    if not email or not pw:
        return json_response(errno=ErrCode.SIGNUP_FAILED, msg='Email and password are required.')
    try:
        service = AccountService.signup(email, pw)
        if not service:
            return json_response(errno=ErrCode.EMAIL_EXIST, msg=f'Email {email} already exists.')
        resp = json_response(msg=f'Signup successfully. '
                             f'We have send a email to {email}.')
        return set_token(service, resp)
    except Exception as ex:
        logger.warning(f'Occured an exception when signup with {email}. {ex}')
        return json_response(errno=ErrCode.SIGNUP_FAILED, msg='Invalid email or password.')


@routes.post('/logout')
async def logout(_: Request):
    resp = json_response()
    resp.set_cookie('token', '', httponly=True,
                    expires="Thu, 01 Jan 1970 00:00:00 GMT")
    return resp


@routes.post('/init')
async def init(request: Request):
    data = request.post()


if __name__ == '__main__':
    app = web.Application(middlewares=[base_exception_middleware])
    aiohttp_jinja2.setup(app, loader=jinja2.FileSystemLoader('./templates'))
    app.add_subapp('/email', email_app)
    app.add_subapp('/query', query_app)
    app.add_subapp('/account', account_app)
    routes.static('/', 'static')
    app.add_routes(routes)
    web.run_app(app)
