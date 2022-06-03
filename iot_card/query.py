import json
import random

import aiohttp
from al_utils.alru import alru_cache
from al_utils.logger import Logger

from iot_card.model import DigestModel

logger = Logger(__file__).logger


class Query:
    def __init__(self, card_id: int | str, session: aiohttp.ClientSession) -> None:
        self.card_id = card_id
        self.session = session

    @alru_cache
    async def login(self) -> dict:
        async with self.session.post(f'http://iotcz.miyilink.com/kyhl-weixin-1.0/card/login.do?'
                                     f'responseFunction=findByiccidMarkCallback&'
                                     f'iccidMark={self.card_id}') as resp:
            if resp.status == 200:
                logger.info(f'Network request successfully '
                            f'when login with status {resp.status}')
                content = await resp.text()
                return json.loads(content)
            logger.warn(f'Network request failed '
                        f'when login with status {resp.status}')

    @alru_cache
    async def get_account(self) -> dict:
        """Get raw response of card info."""
        async with self.session.post(f'http://iotcz.miyilink.com/kyhl-weixin-1.0/user/findByOpenId.do?'
                                     f'responseFunction='
                                     f'findByOpenIdCallback&rfm={random.random()}'
                                     ) as resp:
            if resp.status == 200:
                logger.info(f'Network request successfully '
                            f'when get account with status {resp.status}')
                content = await resp.text()
                return json.loads(content)
            logger.warn(f'Network request failed '
                        f'when get account with status {resp.status}')

    @alru_cache
    async def get_usage(self) -> dict:
        """Get raw response of usage of card's data."""
        async with self.session.post(f'http://iotcz.miyilink.com/kyhl-weixin-1.0/card/findCardInfo.do?'
                                     f'iccidOrPhone=&'
                                     f'responseFunction=findCardInfoCallback1&'
                                     f'rfm={random.random()}'
                                     ) as resp:
            if resp.status == 200:
                logger.info(f'Network request successfully '
                            f'when get usage with status {resp.status}')
                content = await resp.text()
                return json.loads(content)
            logger.warn(f'Network request failed '
                        f'when get usage with status {resp.status}')

    @alru_cache
    async def get_digest(self) -> DigestModel:
        account = await self.get_account()
        usage = await self.get_usage()
        digest = DigestModel()
        digest["balance"] = account["walletEntity"]["moneyBalance"]
        digest["iccid"] = usage["cardLiftList"][0]["iccidMark"]
        digest["card"] = self.card_id
        digest["phone"] = usage["cardLiftList"][0]["phone"]
        digest["isp"] = usage["entity"]["categoryStr"]
        digest["plan"] = usage["cardLiftList"][0]["mealName"]
        digest["status"] = usage["entity"]["statusStr"]
        digest["expired"] = usage["entity"]["expireDate"]
        digest["total"] = float(usage["cardLiftList"][0]["flowSize"])
        digest["usage"] = float(usage["entity"]["totalBytesCnt"])
        digest["renewal"] = bool(usage["nextCardLifeList"])
        return digest

    async def logout(self):
        """Clear session cookies."""
        self.session.cookie_jar.clear()

    def clear_cache(self):
        """Clear all cached result which wrapped in :func:`alru_cache`"""
        for fn in [self.login, self.get_account, self.get_usage, self.get_digest]:
            fn.cache_clear()

    def __del__(self):
        self.session.close()
