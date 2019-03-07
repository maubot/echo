from collections import deque
from typing import Optional, Deque
from time import time

from mautrix.types import EventID, TextMessageEventContent, MessageType

from maubot import Plugin, MessageEvent
from maubot.handlers import command

DEDUP_SIZE_CAP: int = 5


class EchoBot(Plugin):
    dedup: Deque[EventID]

    async def start(self):
        await super().start()
        self.dedup = deque(maxlen=DEDUP_SIZE_CAP)

    @staticmethod
    def plural(num: float, unit: str, decimals: Optional[int] = None) -> str:
        num = round(num, decimals)
        if num == 1:
            return f"{num} {unit}"
        else:
            return f"{num} {unit}s"

    @classmethod
    def prettify_diff(cls, diff: int) -> str:
        if abs(diff) < 10 * 1_000:
            return f"{diff} ms"
        elif abs(diff) < 60 * 1_000:
            return cls.plural(diff / 1_000, 'second', decimals=1)
        minutes, seconds = divmod(diff / 1_000, 60)
        if abs(minutes) < 60:
            return f"{cls.plural(minutes, 'minute')} and {cls.plural(seconds, 'second')}"
        hours, minutes = divmod(minutes, 60)
        if abs(hours) < 24:
            return (f"{cls.plural(hours, 'hour')}, {cls.plural(minutes, 'minute')}"
                    f" and {cls.plural(seconds, 'second')}")
        days, hours = divmod(hours, 24)
        return (f"{cls.plural(days, 'day')}, {cls.plural(hours, 'hour')},"
                f"{cls.plural(minutes, 'minute')} and {cls.plural(seconds, 'second')}")

    @command.new("ping", help="Ping")
    async def ping_handler(self, evt: MessageEvent) -> None:
        diff = int(time() * 1000) - evt.timestamp
        if evt.event_id not in self.dedup:
            self.dedup.append(evt.event_id)
            content = TextMessageEventContent(msgtype=MessageType.NOTICE,
                                              body="Pong! (ping took "
                                              f"{self.prettify_diff(diff)} to arrive)")
            content["pong"] = {
                "ms": diff,
                "from": evt.sender.split(":", 1)[1],
                "ping": evt.event_id,
            }
            await evt.reply(content)

    @command.new("echo", help="Repeat a message")
    @command.argument("message", pass_raw=True)
    async def echo_handler(self, evt: MessageEvent, message: str) -> None:
        if evt.event_id not in self.dedup:
            self.dedup.append(evt.event_id)
            await evt.respond(message)
