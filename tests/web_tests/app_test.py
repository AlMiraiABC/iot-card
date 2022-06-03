from unittest.mock import patch
from aiohttp import FormData
from services.account_service import AccountService
import aiohttp.web as aioweb
from aiohttp.test_utils import AioHTTPTestCase
from app import routes


@patch.object(AccountService, '__init__', lambda *_, **__: None)
@patch.object(AccountService, 'create_token', lambda *_: 'testtoken')
class TestApp(AioHTTPTestCase):

    async def get_application(self):
        app = aioweb.Application()
        app.add_routes(routes)
        return app

    @patch.object(AccountService, 'create_token', lambda *_: 'testtoken')
    @patch.object(AccountService, 'login', lambda *_: AccountService())
    async def test_login(self):
        data = FormData({'email': 'test@example.com',
                        'password': 'testpassword'})
        async with self.client.post("/login", data=data) as resp:
            self.assertEqual(resp.status, 200)
            result = await resp.json()
            self.assertTrue(result['success'])
            self.assertIn(resp.cookies['token'].value, 'testtoken')

    @patch.object(AccountService, 'login', lambda *_: None)
    async def test_login_fail(self):
        data = FormData({'email': 'test@example.com',
                        'password': 'testpassword'})
        async with self.client.post("/login", data=data) as resp:
            self.assertEqual(resp.status, 200)
            result = await resp.json()
            self.assertFalse(result['success'])

    @patch.object(AccountService, 'signup', lambda *_: AccountService)
    async def test_signup(self):
        data = FormData({'email': 'test@example.com',
                        'password': 'testpassword'})
        async with self.client.post("/signup", data=data) as resp:
            self.assertEqual(resp.status, 200)
            result = await resp.json()
            self.assertTrue(result['success'])
            self.assertIn(resp.cookies['token'].value, 'testtoken')

    @patch.object(AccountService, 'signup', lambda *_: None)
    async def test_signup_fail(self):
        data = FormData({'email': 'test@example.com',
                        'password': 'testpassword'})
        async with self.client.post("/signup", data=data) as resp:
            self.assertEqual(resp.status, 200)
            result = await resp.json()
            self.assertFalse(result['success'])
