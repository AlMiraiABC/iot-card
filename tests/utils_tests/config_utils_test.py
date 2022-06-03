from unittest import TestCase
from unittest.mock import patch

from utils.config import Config
from utils.config_utils import (AccountConfigUtil, AppConfigUtil,
                                EmailConfigUtil)


@patch.object(AccountConfigUtil, '__init__', lambda *_: None)
@patch.object(Config, '__init__', lambda *_: None)
@patch.object(Config, 'save', lambda *_: None)
class TestAccountConfigUtil(TestCase):

    def test_add_unexist(self):
        util = AccountConfigUtil()
        util.accounts = [
            {
                "email": "email1"
            }
        ]
        util.add({'email': 'email2'})
        self.assertListEqual(util.accounts, [
            {
                'email': 'email1'
            },
            # added receiver is formated
            {
                'cards': [],
                'email': 'email2',
                'freq': 7,
                'last_time': None,
                'name': ''
            }
        ])

    def test_add_update(self):
        util = AccountConfigUtil()
        util.accounts = [
            {
                "email": "email1"
            },
            {
                'email': 'email2'
            }
        ]
        util.add(
            {
                'email': 'email2',
                'last_time': '2022',
                'freq': 7
            }
        ),
        self.assertListEqual(util.accounts, [
            {
                "email": "email1"
            },
            {
                'cards': [],
                'email': 'email2',
                'freq': 7,
                'last_time': '2022',
                'name': ''
            }
        ])

    def test_add_err(self):
        util = AccountConfigUtil()
        with self.assertRaises(ValueError):
            util.add({})

    def test_get_empty(self):
        util = AccountConfigUtil()
        util.receivers = []
        ret = util.get('')
        self.assertTupleEqual(ret, (None, None))

    def test_get_exist(self):
        util = AccountConfigUtil()
        util.accounts = [
            {
                'email': 'email1'
            },
            {
                'email': 'email2'
            }
        ]
        ret = util.get('email2')
        self.assertEqual(ret[0]['email'], util.accounts[1]['email'])
        self.assertEqual(ret[1], 1)

    def test_get_unexist(self):
        util = AccountConfigUtil()
        util.receivers = [
            {
                'email': 'email1'
            },
            {
                'email': 'email2'
            }
        ]
        ret = util.get('email3')
        self.assertTupleEqual(ret, (None, None))


@patch.object(EmailConfigUtil, '__init__', lambda *_, **__: None)
@patch.object(Config, '__init__', lambda *_: None)
@patch.object(Config, 'save', lambda *_: None)
class TestEmailConfigUtil(TestCase):
    def test_init(self):
        util = EmailConfigUtil()
        util.sender = {'email': 'sender_email'}
        util.server = {'host': 'host', 'passcode': 'passcode'}
        util.receivers = [{'email': 'rec_email'}]
        util.init()
        print(util.server)
        print(util.sender)
        print(util.receivers)
        self.assertEqual(util.sender['name'], '')
        self.assertEqual(util.server['username'], util.sender['email'])
        self.assertEqual(util.server['ssl'], True)
        self.assertEqual(util.server['port'], 465)
        self.assertEqual(util.receivers[0]['email'], 'rec_email')

    def test_init_key_err(self):
        util = EmailConfigUtil()
        util.sender = {}
        with self.assertRaises(KeyError):
            util.init()


@patch.object(AppConfigUtil, '__init__', lambda *_: None)
@patch.object(Config, '__init__', lambda *_: None)
@patch.object(Config, '__init__', lambda *_: None)
class TestAppConfigUtil(TestCase):

    def test_init(self):
        util = AppConfigUtil()
        util.config = {}
        util.init()
        print(util.config)
        self.assertIsNotNone(util.config['salt'])
        self.assertEqual(util.config['token_alg'], 'HS256')
        self.assertEqual(util.config['def_freq'], 7)
        self.assertEqual(util.config['login_exp'], 3600)
