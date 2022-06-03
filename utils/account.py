import random
import string

import bcrypt
from al_utils.logger import Logger
from al_utils.singleton import Singleton
from services.email_service import EmailService, get_configured_email

from utils.config import AccountConfig
from utils.config_utils import AccountConfigUtil


def hash_pw(plain: str) -> str:
    """
    Hash :param:`plain`

    :param plain: Plain text.
    """
    passwd = plain.encode()
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(passwd, salt)
    return hashed.decode()


def check_pw(plain: str, hashed: str) -> bool:
    """
    Determine whether password is correct.

    :param plain: Plain text. original password.
    :param hashed: Hashed password.
    """
    bpw = plain.encode()
    bhash = hashed.encode()
    return bcrypt.checkpw(bpw, bhash)


def gen_password(length: int = 18):
    """Generate a random string with specified :param:`length`"""
    return ''.join(random.choices(
        string.ascii_letters+string.digits + '!@$_', k=length))


logger = Logger(__file__).logger


class Account:
    def __init__(self, email: str) -> None:
        if not email:
            raise ValueError(f'Email cannot be empty. But got `{email}`')
        self.email = email
        self.config = AccountConfigUtil().get(self.email)[0]
        if not self.config:
            raise ValueError(
                f"Email {self.email} doesn't exist. Please create it firstly.")

    @classmethod
    def new_account(cls, email_address: str, password: str, **kwargs):
        """
        Create a new account.

        :param email_account: The email address to create.
        :param password: The password plain text.
        :param **kwargs: Additional account configs
        :return: Account if created. Otherwise None if :param:`email` exists.
        """
        if not email_address:
            return None
        if AccountConfigUtil().get(email_address):
            return None
        hashed = hash_pw(password)
        account = AccountConfig(
            email=email_address, password=hashed, **kwargs)
        AccountConfigUtil.add(account)
        get_configured_email().send('IOT Card Create New Account',
                                    f'You registered a new account just now.')
        return cls(email_address)

    def reset_password(self, cur_password: str, new_password: str):
        """
        Reset password to :param:`new_password` of current account if :param:`cur_password` is correct.

        :param cur_password: Current password plain text.
        :param new_password: New password plain text.
        :return: Config after reset. Otherwise None.
        """
        if not self.valid_password(cur_password):
            return None
        hashed = hash_pw(new_password)
        self.config['password'] = hashed
        AccountConfigUtil().add(self.config)
        get_configured_email().send('IOT Card Reset Password',
                                    f'Reset password just now.')
        return self.config

    def valid_password(self, password: str):
        return check_pw(password, self.config['password'])
