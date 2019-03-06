from time import time

from maubot import Plugin, MessageEvent
from maubot.handlers import command


class EchoBot(Plugin):
    @staticmethod
    def time_since(ms: int) -> str:
        diff = int(time() * 1000) - ms
        if abs(diff) < 10 * 1_000:
            return f"{diff} ms"
        elif abs(diff) < 60 * 1_000:
            return f"{round(diff / 1_000, 1)} seconds"
        minutes, seconds = divmod(diff / 1_000, 60)
        seconds = round(seconds)
        if abs(minutes) < 60:
            return f"{minutes} minutes and {seconds} seconds"
        hours, minutes = divmod(minutes, 60)
        if abs(hours) < 24:
            return f"{hours} hours, {minutes} minutes and {seconds} seconds"
        days, hours = divmod(hours, 24)
        return f"{days} days, {hours} hours, {minutes} minutes and {seconds} seconds"

    @command.new("ping", help="Ping")
    async def ping_handler(self, evt: MessageEvent) -> None:
        await evt.reply(f"Pong! (ping took {self.time_since(evt.timestamp)} to arrive)")

    @command.new("echo", help="Repeat a message")
    @command.argument("message", pass_raw=True)
    async def echo_handler(self, evt: MessageEvent, message: str) -> None:
        await evt.respond(message)
