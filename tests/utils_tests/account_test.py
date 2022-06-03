from unittest import TestCase
from unittest.mock import patch

import bcrypt
from services.email_service import EmailService

import utils.account
from utils.account import Account, hash_pw
from utils.config import Config
from utils.config_utils import AccountConfigUtil
from utils.email import Email


@patch.object(utils.account, 'get_configured_email', lambda *_, **__: Email())
@patch.object(AccountConfigUtil, '__init__', lambda *_, **__: None)
@patch.object(Email, '__init__', lambda *_, **__: None)
@patch.object(Config, '__init__', lambda *_, **__: None)
@patch.object(Config, 'save', lambda *_: None)
@patch.object(Account, '__init__', lambda *_, **__: None)
class TestAccount(TestCase):

    @patch.object(AccountConfigUtil, 'get', lambda *_, **__: (None, None))
    @patch.object(AccountConfigUtil, 'add', lambda *_, **__: None)
    def test_new_account(self):
        account = Account.new_account('test@example.com', 'testpassword')
        self.assertIsNotNone(account)

    @patch.object(AccountConfigUtil, 'get', lambda *_, **__: (None, None))
    @patch.object(AccountConfigUtil, 'add', lambda *_, **__: None)
    def test_new_account_empty_email(self):
        account = Account.new_account('', '')
        self.assertIsNone(account)

    @patch.object(AccountConfigUtil, 'get', lambda *_, **__: ({'email': 'test@example.com'}, None))
    @patch.object(AccountConfigUtil, 'add', lambda *_, **__: None)
    def test_new_account_exists(self):
        account = Account.new_account('test@example.com', 'testpassword')
        self.assertIsNone(account)

    @patch.object(AccountConfigUtil, 'get', lambda *_, **__: ({'email': 'test@example.com', 'password': 'hashednewpassword'}, 1))
    @patch.object(AccountConfigUtil, 'add', lambda *_, **__: None)
    def test_new_account(self):
        PW = 'testpassword'
        NPW = 'newpw'
        account = Account()
        account.config = {'password': hash_pw(PW)}
        account.email = 'test@example.com'
        ret = account.reset_password(PW, NPW)
        self.assertTrue(bcrypt.checkpw(NPW.encode(), ret['password'].encode()))

    @patch.object(AccountConfigUtil, 'get', lambda *_, **__: ({'email': 'test@example.com', 'password': 'hashednewpassword'}, 1))
    @patch.object(AccountConfigUtil, 'add', lambda *_, **__: None)
    def test_new_account_wrong_pw(self):
        PW = 'testpassword'
        account = Account()
        account.config = {'password': hash_pw(PW)}
        account.email = 'test@example.com'
        ret = account.reset_password(PW+'abcdefg', 'newpw')
        self.assertIsNone(ret)

    def test_valid_password(self):
        PW = 'testpassword'
        account = Account()
        account.config = {'password': hash_pw(PW)}
        ret = account.valid_password(PW)
        self.assertTrue(ret)

    def test_valid_password_false(self):
        PW = 'testpassword'
        account = Account()
        account.config = {'password': hash_pw(PW)}
        ret = account.valid_password(PW+'abcdefg')
        self.assertFalse(ret)
