import json
import os
from typing import Literal, TypedDict

from al_utils.logger import Logger
from al_utils.singleton import Singleton


class ServerConfig(TypedDict):
    host: str
    port: str
    username: str
    passcode: str
    ssl: bool


class SenderConfig(TypedDict):
    email: str
    name: str


class ReceiverConfig(TypedDict):
    email: str
    name: str
    password: str
    freq: int
    last_time: str
    cards: list[str]


AccountConfig = ReceiverConfig


ReceiversConfig = list[ReceiverConfig]


class EmailConfig(TypedDict):
    server: ServerConfig
    sender: SenderConfig
    receivers: ReceiversConfig


class AppConfig(TypedDict):
    salt: str
    token_alg: Literal['HS256']
    def_freq: int


class ManagerConfig(TypedDict):
    email: str
    name: str
    password: str


logger = Logger(__file__).logger


class Config(Singleton):
    def __init__(self, file: str = './config.json') -> None:
        self.file = file or './config.json'
        logger.debug(f'Set config file {self.file}')
        self.check_file()
        self.config = self.get_config()
        self.init()
        self.save()

    def check_file(self, file: str = None, create: bool = True, default_content: str = '{}'):
        file = file or self.file
        if os.path.exists(file) and os.path.isdir(file):
            raise ValueError(
                f'{self.file} exists but not a file. Please remove it.')
        if not os.path.exists(file) and create:
            with open(file, 'w', encoding='utf-8') as f:
                f.write(default_content)
            logger.info(
                f'Create config file {file} and write {default_content}')

    def get_config(self) -> dict:
        self.check_file(create=False)
        with open(self.file, 'r', encoding='utf-8') as f:
            return json.load(f)

    def save(self):
        self.check_file()
        with open(self.file, 'w', encoding='utf-8') as f:
            json.dump(self.config, f)
        logger.info(f'Save config file {self.file} successfully.')

    def init(self):
        """Initialize the configuration file."""
        # region app
        if 'app' not in self.config:
            self.config['app'] = {}
        if 'manager' not in self.config:
            self.config['manager'] = {}
        if 'email' not in self.config:
            self.config['email'] = {}
        email: EmailConfig = self.config['email']
        if 'sender' not in email:
            email['sender'] = {}
        if 'server' not in email:
            email['server'] = {}
        if 'receivers' not in email:
            email['receivers'] = []
