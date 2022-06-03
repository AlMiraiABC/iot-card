import time
from typing import TypedDict

import jwt
from al_utils.logger import Logger
from utils.account import Account
from utils.config_utils import AppConfigUtil

logger = Logger(__file__).logger


class TokenNotFound(Exception):
    pass


class TokenPayload(TypedDict):
    email: str
    exp: int


class AccountService:

    def __init__(self, email: str, token: str = None) -> None:
        """
        :param email: The email address of account.
        :param token: The JWT token.
        """
        self.account = Account(email)
        self.config = self.account.config
        self.email = email
        self.token = token
        self.app_config = AppConfigUtil().config

    def _check_login(self):
        """
        Determine whether this account has jwt token.

        :raise TokenNotFound: Cannot find jwt token.
        """
        if not self.token:
            raise TokenNotFound('Token not found. Please login first.')

    @classmethod
    def login(cls, email: str, password: str):
        try:
            service = cls(email)
            if service.account.valid_password(password):
                service.token = service.create_token()
                return service
        except Exception as ex:
            logger.warn(f'Log in failed with email {email}, {ex}')
        return None

    @classmethod
    def signup(cls, email: str, password: str):
        try:
            cls(email)
            return None
        except ValueError:
            account = Account.new_account(email, password)
            if not account:
                return None
            return cls(email)

    def create_token(self):
        salt = self.app_config['salt']
        alg = self.app_config['token_alg']
        payload: TokenPayload = {
            "email": self.email,
            "exp": int(time.time())+self.app_config['login_exp']
        }
        self.token = jwt.encode(payload, salt, alg)
        return self.token

    @classmethod
    def valid_token(cls, token: str) -> TokenPayload:
        salt = AppConfigUtil().config['salt']
        alg = AppConfigUtil().config.get('token_alg', 'HS256')
        return jwt.decode(token, salt, [alg])
