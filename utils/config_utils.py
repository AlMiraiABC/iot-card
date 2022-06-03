import bcrypt
from al_utils.logger import Logger
from al_utils.singleton import Singleton

from utils.config import (AccountConfig, AppConfig, Config, EmailConfig,
                          ManagerConfig, ReceiverConfig)

logger = Logger(__file__).logger


class AccountConfigUtil(Singleton):
    def __init__(self) -> None:
        email_config: EmailConfig = Config().config['email']
        self.accounts = [self.format_account(rec)
                         for rec in email_config['receivers']]

    @classmethod
    def format_account(cls, account: AccountConfig) -> AccountConfig:
        account = account or {}
        account['email']
        account['name'] = account.get('name', '')
        account['freq'] = account.get('freq', 7)
        account['last_time'] = account.get('last_time', None)
        account['cards'] = account.get('cards', [])
        return account

    def add(self, account: AccountConfig):
        """
        Add a account to config or update it if email exists.

        :param account: Add it if email doesn't exist. Or update other keys if not None.
        :raises ValueError: account.email cannot be empty.
        """
        if not account.get('email'):
            raise ValueError('email must be set')

        account = self.format_account(account)
        user, _ = self.get(account['email'])
        if not user:
            self.accounts.append(account)
            logger.info(f"account {account['email']} doesn't exist, "
                        f"add it. {account}")
        else:
            before = user.copy()
            for k, v in account.items():
                user[k] = v if v is not None else user[k]
                logger.debug(f"update key {k} to {user[k]}")
            logger.info(f"account {account['email']} exists, "
                        f"update {before} to {user}")
        Config().save()

    def get(self, email: str) -> tuple[AccountConfig | None, int | None]:
        """
        Get account by :param:`email`.

        :param email: The email address of account.
        :returns: The first item is matched account which email is :param:`email`, or None if not found.
                    The second item is matched account's index in email.receivers, or None if not found.
        """
        if not self.accounts:
            return None, None
        for index, account in enumerate(self.accounts):
            if account['email'] == email:
                return account, index
        return None, None

    def delete(self, email: str):
        """Remove this account if exists."""
        if not email:
            return
        index = self.get(email)[1]
        if index is None:
            return
        self.accounts.pop(index)
        Config().save()


class EmailConfigUtil(Singleton):
    def __init__(self):
        self.config: EmailConfig = Config().config['email']
        self.server = self.config['server']
        self.sender = self.config['sender']
        self.receivers = self.config['receivers']
        self.init()
        Config().save()

    def init(self):
        """Initialize config.email"""
        # region sender
        self.sender['email']
        self.sender['name'] = self.sender.get('name', '')
        # endregion sender
        # region server
        self.server['host']
        self.server['passcode']
        self.server['username'] = self.server.get(
            'username', self.sender['email'])
        self.server['ssl'] = self.server.get('ssl', True)
        self.server['port'] = self.server.get(
            'port', 465 if self.server['ssl'] else 25)
        # endregion
        # region receivers
        self.receivers = [AccountConfigUtil.format_account(rec)
                          for rec in self.receivers]
        # endregion

    def add_receiver(self, receiver: ReceiverConfig):
        """Add or update a receiver."""
        return AccountConfigUtil().add(receiver)

    def del_receiver(self, email: str):
        return AccountConfigUtil().delete(email)

    def get_receiver(self, email: str):
        return AccountConfigUtil().get(email)

    def get_receivers(self):
        return self.receivers


class AppConfigUtil:
    def __init__(self) -> None:
        self.config: AppConfig = Config().config['app']
        self.init()
        Config().save()

    def init(self):
        if 'salt' not in self.config:
            self.config['salt'] = bcrypt.gensalt().decode()
        if 'token_alg' not in self.config:
            self.config['token_alg'] = 'HS256'
        if 'def_freq' not in self.config:
            self.config['def_freq'] = 7
        if 'login_exp' not in self.config:
            self.config['login_exp'] = 3600

    def update(self, salt: str = None, token_alg: str = None, def_freq: int = None, login_exp: int = None):
        if not salt:
            self.config['salt'] = salt
        if not token_alg:
            self.config['token_alg'] = token_alg
        if not def_freq:
            self.config['def_freq'] = def_freq
        if not login_exp:
            self.config['login_exp'] = login_exp
        Config().save()


class ManagerConfigUtil:
    def __init__(self) -> None:
        self.config: ManagerConfig = Config().config['manager']

    def is_init(self) -> bool:
        return bool(self.config)

    def update(self, name: str, email: str, password: str):
        if not email:
            raise ValueError('name cannot be empty.')
        if not password:
            raise ValueError('password cannot be empty.')
        if not name:
            name = email
        self.config['name'] = name
        self.config['email'] = email
        self.config['password'] = password
        Config().save()
