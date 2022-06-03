import asyncio
import sys
from services.email_service import EmailService
from al_utils.console import ColoredConsole

if __name__ == '__main__':
    service = EmailService()
    args = sys.argv[1:]
    if args[0] == 'email':
        if len(args) == 1:
            s, f, p = asyncio.run(service.send_all())
            for r, c in s:
                ColoredConsole.success(f'Successed: Send {c} to {r["email"]}')
            for r, c in f:
                ColoredConsole.error(f'Failed: Send {c} to {r["email"]}')
            for r in f:
                ColoredConsole.debug(f'Passed: {r}')
