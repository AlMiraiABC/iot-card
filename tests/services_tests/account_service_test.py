from unittest import TestCase
from unittest.mock import patch

import jwt
from services.account_service import AccountService, TokenNotFound
from utils.account import Account, hash_pw
from utils.config_utils import AppConfigUtil


@patch.object(AccountService, '__init__', lambda *_, **__: None)
@patch.object(Account, '__init__', lambda *_, **__: None)
class TestAccountService(TestCase):
    def test__check_login_no_token(self):
        service = AccountService()
        service.token = None
        with self.assertRaises(TokenNotFound):
            service._check_login()

    def test__check_login(self):
        service = AccountService()
        service.token = 'tokentestabc'
        service._check_login()

    @patch.object(AccountService, 'create_token', lambda *_: "mock token")
    def test_login(self):
        PW = 'testpassword'
        account = Account()
        account.config = {'password': hash_pw(PW)}
        service = AccountService()  # class method shouldn't init
        service.account = account
        ret = service.login('test@example.com', PW)
        self.assertTrue(ret)

    def test_login_failed(self):
        PW = 'testpassword'
        account = Account()
        account.config = {'password': hash_pw(PW)}
        service = AccountService()
        service.account = account
        ret = service.login('test@example.com', PW+'abcdefg')
        self.assertFalse(ret)

    @patch.object(AppConfigUtil, '__init__', lambda *_, **__: None)
    def test_create_token(self):
        SALT = '123'
        EMAIL = 'test@example.com'
        service = AccountService()
        service.email = EMAIL
        service.app_config = {'login_exp': 10,
                              'salt': SALT, 'token_alg': 'HS256'}
        token = service.create_token()
        ret = jwt.decode(token, SALT, ['HS256'])
        self.assertEqual(ret['email'], EMAIL)
