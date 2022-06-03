from datetime import datetime, timedelta
from unittest import IsolatedAsyncioTestCase
from unittest.mock import patch

from iot_card.query import Query
from services.email_service import EmailService
from utils.config import Config
from utils.email import Email


async def mock_func(*_, **__):
    return None


@patch.object(EmailService, '__init__', lambda *_: None)
class TestEmailService(IsolatedAsyncioTestCase):
    def test_should_send(self):
        service = EmailService()
        ret = service.should_send(
            {
                'last_time': (datetime.now()-timedelta(10)).isoformat(),
                'freq': 7
            }
        )
        self.assertTrue(ret)

    def test_should_not_send(self):
        service = EmailService()
        ret = service.should_send(
            {
                'last_time': (datetime.now()-timedelta(1)).isoformat(),
                'freq': 7
            }
        )
        self.assertFalse(ret)

    def test_should_send_empty(self):
        service = EmailService()
        ret = service.should_send({})
        self.assertFalse(ret)

    @patch.object(Email, '__init__', lambda *_, **__: None)
    @patch.object(Email, 'send', lambda *_, **__: (True, None))
    @patch.object(Query, 'login', mock_func)
    @patch.object(Query, 'get_digest', mock_func)
    async def test_send_all(self):
        service = EmailService()
        service.email = Email()
        service.sender = {
            'email': 'sender_email',
            'name': 'Sender'
        }
        service.server = {
            'host': 'host',
            'port': 123,
            'username': 'sender_email',
            'passcode': 'abcdefg',
            'ssl': True
        }
        service.receivers = [
            {
                'email': 'email1',
                'cards': ['1', '2'],
                'name':'rec1',
                'freq':1,
                'last_time':(datetime.now()-timedelta(2)).isoformat()
            },
            {
                'email': 'email2',
                'cards': ['3', '4'],
                'name':'rec1',
                'freq':7,
                'last_time':(datetime.now()-timedelta(2)).isoformat()
            }
        ]
        s, f, p = await service.send_all()
        self.assertListEqual(s, [
            (service.receivers[0], '1'),
            (service.receivers[0], '2'),
        ])
        self.assertListEqual(f, [])
        self.assertListEqual(p, [
            service.receivers[1],
        ])


class TestEmailServiceRun(IsolatedAsyncioTestCase):
    async def test_send_all(self):
        service = EmailService()
        s, f, p = await service.send_all()
        print(s)
        print(f)
        print(p)
