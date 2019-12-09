from typing import Optional
from time import time
from html import escape

from mautrix.types import TextMessageEventContent, MessageType, Format

from maubot import Plugin, MessageEvent
from maubot.handlers import command


class EchoBot(Plugin):
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
        return (f"{cls.plural(days, 'day')}, {cls.plural(hours, 'hour')}, "
                f"{cls.plural(minutes, 'minute')} and {cls.plural(seconds, 'second')}")

    @command.new("ping", help="Ping")
    @command.argument("message", pass_raw=True, required=False)
    async def ping_handler(self, evt: MessageEvent, message: str = "") -> None:
        diff = int(time() * 1000) - evt.timestamp
        pretty_diff = self.prettify_diff(diff)
        text_message = f'"{message[:20]}" took' if message else "took"
        html_message = f'"{escape(message[:20])}" took' if message else "took"
        content = TextMessageEventContent(
            msgtype=MessageType.NOTICE, format=Format.HTML,
            body=f"{evt.sender}: Pong! (ping {text_message} {pretty_diff} to arrive)",
            formatted_body=f"<a href='https://matrix.to/#/{evt.sender}'>{evt.sender}</a>: Pong! "
            f"(<a href='https://matrix.to/#/{evt.room_id}/{evt.event_id}'>ping</a> {html_message} "
            f"{pretty_diff} to arrive)")
        content["pong"] = {
            "ms": diff,
            "from": evt.sender.split(":", 1)[1],
            "ping": evt.event_id,
        }
        content["m.relates_to"] = {
            "rel_type": "xyz.maubot.pong",
            "event_id": evt.event_id,
            "from": evt.sender.split(":", 1)[1],
            "ms": diff,
        }
        await evt.respond(content)

    @command.new("echo", help="Repeat a message")
    @command.argument("message", pass_raw=True)
    async def echo_handler(self, evt: MessageEvent, message: str) -> None:
        await evt.respond(message)
