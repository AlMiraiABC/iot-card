import os
from unittest import IsolatedAsyncioTestCase

import aiohttp
from iot_card.query import Query

FAIL_CARD_ID = 1


class TestQueryLogin(IsolatedAsyncioTestCase):
    async def asyncSetUp(self) -> None:
        self.session = aiohttp.ClientSession()
        return await super().asyncSetUp()

    async def test_login(self):
        query = Query(os.environ.get("IOT_CARD"), self.session)
        resp = await query.login()
        self.assertTrue(resp.get('entity'))

    async def test_login_fail(self):
        query = Query(FAIL_CARD_ID, self.session)
        resp = await query.login()
        self.assertFalse(resp.get('entity'))


class TestQueryGet(IsolatedAsyncioTestCase):
    async def asyncSetUp(self) -> None:
        session = aiohttp.ClientSession()
        self.query = Query(os.environ.get("IOT_CARD"), session)
        await self.query.login()
        return await super().asyncSetUp()

    async def asyncTearDown(self) -> None:
        await self.query.logout()
        return await super().asyncTearDown()

    async def test_get_account(self):
        resp = await self.query.get_account()
        self.assertEqual(resp.get('isSuccess'), '0')

    async def test_get_usage(self):
        resp = await self.query.get_usage()
        self.assertTrue(resp.get('entity'))

    async def test_get_digest(self):
        resp = await self.query.get_digest()
        self.assertIsNotNone(resp)
