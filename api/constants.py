from enum import Enum
from aiohttp.web import json_response as response


class ErrCode(Enum):
    SUCCESS = (000, 'Success')
    # account
    EMAIL_NOT_FOUND = (101, 'Email not found')
    EMAIL_EXIST = (102, 'Email already exists')
    LOGIN_FAILED = (111, 'Login failed')
    SIGNUP_FAILED = (121, 'Signup failed')
    # email
    SEND_FAILED = (201, 'Send email failed')
    # init
    INIT_FAILED = (301, 'Initialization failed')
    INITED = (302, 'App has been initialized')


def json_response(errno: ErrCode = ErrCode.SUCCESS, msg: str = '', data: object = None):
    success = errno == ErrCode.SUCCESS
    return response({'success': success, 'msg': msg or errno.value[1], 'data': data, 'errno': errno.value[0]})
