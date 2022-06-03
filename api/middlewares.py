from aiohttp.web import Response, middleware
from aiohttp.web_exceptions import (HTTPClientError, HTTPRedirection,
                                    HTTPServerError, HTTPSuccessful,
                                    HTTPUnauthorized)
from aiohttp.web_middlewares import Handler
from aiohttp.web_request import Request
from al_utils.logger import Logger
from services.account_service import AccountService

ACCOUNT_STORAGE = '_account'

logger = Logger(__file__).logger


@middleware
async def login_middleware(request: Request, handler: Handler):

    def get_token_query():
        """Get token from request query parameters: token=<token>"""
        return request.query.get('token')

    def get_token_req():
        """Get token from request storage"""
        return request.get('token')

    def get_token_header():
        """Get token from request header: `Authorization: Bearer <token>"""
        auth = request.headers.get('Authorization')
        if auth:
            if auth.startswith('Bearer '):
                token = token[7:]

    def get_token_cookie():
        return request.cookies.get('token')

    for m in [get_token_query, get_token_req, get_token_header, get_token_cookie]:
        token = m()
        if token:
            break
    if not token:
        logger.warn(f'Token not found. Please login.')
        raise HTTPUnauthorized('Can not get token. Please login.')
    try:
        payload = AccountService.valid_token(token)
        request['_account'] = AccountService(payload['email'], token)
    except Exception as ex:
        logger.warn(f'token verified failed <{token}>. {ex}')
        raise HTTPUnauthorized('Token expired. Please login again.')
    else:
        return await handler(request)


@middleware
async def base_exception_middleware(request: Request, handler: Handler):
    try:
        return await handler(request)
    except (HTTPSuccessful, HTTPRedirection, HTTPClientError) as ex:
        raise ex
    except (HTTPServerError, Exception) as ex:
        logger.error(f'Occured an exception <METHOD: {request.method}> <PATH: {request.path}> <BODY: {await request.text()}>. {ex}')
        return Response(status=400, reason=f'Occured an exception when visit {request.path}. {ex}')
