from datetime import datetime

import aiohttp
from al_utils.logger import Logger
from iot_card.query import Query
from utils.config import Config, EmailConfig, ReceiverConfig, ReceiversConfig
from utils.config_utils import AccountConfigUtil, EmailConfigUtil
from utils.email import Email

logger = Logger(__file__).logger


def get_configured_email() -> Email:
    config: EmailConfig = Config().config['email']
    server = config['server']
    sender = config['sender']
    email = Email(server['host'], server['username'], server['passcode'],
                  (sender['name'], sender['email']), server['ssl'], server['port'])
    return email


class EmailService(EmailConfigUtil):
    def __init__(self) -> None:
        self.email = get_configured_email()
        super().__init__()

    def should_send(self, receiver: ReceiverConfig) -> bool:
        """
        Determine whether this receiver should send email.

        The days between `last_time` to today is greater than `freq` or `last_time` is None.
        `last_time` is None means haven't sent a email yet.

        The `last_time` must be iso format string.
        """
        if not receiver:
            return False
        last_time = receiver.get('last_time')
        if not last_time:
            return True
        last_time = datetime.fromisoformat(last_time)
        freq = receiver.get('freq', 7)
        if (datetime.today()-last_time).days >= freq:
            return True
        return False

    async def send(self, receiver: ReceiverConfig, card: str):
        receiver = AccountConfigUtil.format_account(receiver)
        if card not in receiver['cards']:
            return False, None
        async with aiohttp.ClientSession() as session:
            query = Query(card, session)
            await query.login()
            return self.email.send('流量卡卡余额提醒', template='./templates/email.j2', subtype='html',
                                   context={'digest': await query.get_digest()},
                                   receivers=[(receiver['name'], receiver['email'])])

    async def send_all(self) -> tuple[list[tuple[ReceiversConfig, str]], list[tuple[ReceiversConfig, str]], list[ReceiversConfig]]:
        """
        Iterator all receivers and try to send email.

        :returns: ((successed, card), (failed, card), passed)
                    The first item is successed receivers and queried card.
                    The second item is failed receivers and queried card, occured error when sent.
                    The third item is passed receivers which shouldn't send.
        """
        successed, failed, passed = [], [], []
        for receiver in self.receivers:
            if not self.should_send(receiver):
                passed.append(receiver)
                continue
            for card in receiver['cards']:
                try:
                    async with aiohttp.ClientSession() as session:
                        query = Query(card, session)
                        await query.login()
                        _, ex = await self.send(receiver, card)
                        if ex:
                            raise ex
                        successed.append((receiver, card))
                except Exception as exception:
                    logger.error(f"occured an exception {exception} to {receiver['email']} "
                                 f"with card {card}")
                    failed.append((receiver, card))
        return successed, failed, passed
