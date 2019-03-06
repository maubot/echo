from typing import Optional
from time import time

from maubot import Plugin, MessageEvent
from maubot.handlers import command


class EchoBot(Plugin):
    @staticmethod
    def plural(num: int, unit: str, decimals: Optional[int] = None) -> str:
        num = round(num, decimals)
        if num == 1:
            return f"{num} {unit}"
        else:
            return f"{num} {unit}s"

    @classmethod
    def time_since(cls, ms: int) -> str:
        diff = int(time() * 1000) - ms
        if abs(diff) < 10 * 1_000:
            return f"{diff} ms"
        elif abs(diff) < 60 * 1_000:
            return cls.plural(diff / 1_000, 'second', decimals=1)
        minutes, seconds = divmod(diff / 1_000, 60)
        if abs(minutes) < 60:
            return f"{cls.plural(minutes, 'minute')} and {cls.plural(seconds, 'second')}"
        hours, minutes = divmod(minutes, 60)
        if abs(hours) < 24:
            return f"{cls.plural(hours, 'hour')}, {cls.plural(minutes, 'minute')} and {cls.plural(seconds, 'second')}"
        days, hours = divmod(hours, 24)
        return f"{cls.plural(days, 'day')}, {cls.plural(hours, 'hour')}, {cls.plural(minutes, 'minute')} and {cls.plural(seconds, 'second')}"

    @command.new("ping", help="Ping")
    async def ping_handler(self, evt: MessageEvent) -> None:
        await evt.reply(f"Pong! (ping took {self.time_since(evt.timestamp)} to arrive)")

    @command.new("echo", help="Repeat a message")
    @command.argument("message", pass_raw=True)
    async def echo_handler(self, evt: MessageEvent, message: str) -> None:
        await evt.respond(message)
