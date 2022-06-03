from email.mime.text import MIMEText
from email.utils import formataddr
import smtplib

from jinja2 import Template

ET = tuple[str | None, str]  # (name, address)


class Email:
    def __init__(self, host: str, username: str, passcode: str, sender: ET, ssl=True, port=465) -> None:
        self.host = host
        self.username = username
        self.passcode = passcode
        self.sender = sender
        self.ssl = ssl
        self.port = port or 465 if ssl else 25

    def send(self, title: str, message: str = '', template: str = '', context: dict = {}, subtype: str = None, receivers: list[ET] = []):
        """
        Send a email to configured receivers. Or do nothing if receivers is empty.

        :param title: The header title
        :param message: The Content body.
        :param template: Path or name of jinja2 template file.
        :param context: Variables in template file.
        :param subtype: Mime type. Such as plain, html ...
        :param receivers: List of receivers.
        :raises ValueError: :param:`message` and :param:`template` cannot be empty at the same time.
        :returns:
            1. execute result
            2. exception if falied.
        """
        receivers = receivers or []
        if not receivers:
            return True, None
        if not message and not template:
            raise ValueError(
                'Message and template cannot be empty at the same time.')
        content: str
        if message:
            content = message
            subtype = subtype or 'plain'
        else:
            with open(template, 'r', encoding='utf-8') as t:
                content = Template(t.read()).render(context)
                subtype = subtype or 'html'
        try:
            msg = MIMEText(content, subtype)
            msg['From'] = formataddr((self.sender[0], self.sender[1]))
            # MIMEText cannot set list directly, and throw `'list' object has no attribute 'encode'`
            # EmailMessage can set list directly and serialized to `To: email1, email2`
            msg['To'] = ','.join([formataddr((r[0], r[1])) for r in receivers])
            msg['Subject'] = title
            if self.ssl:
                smtp = smtplib.SMTP_SSL(self.host, self.port)
            else:
                smtp = smtplib.SMTP(self.host, self.port)
            smtp.login(self.username, self.passcode)
            smtp.send_message(msg)
            smtp.quit()
            return (True, None)
        except Exception as ex:
            return(False, ex)
