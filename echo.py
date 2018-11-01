from time import time

from maubot import Plugin, CommandSpec, Command, Argument, MessageEvent

COMMAND_PING = "ping"
ARG_ECHO = "$echo"
COMMAND_ECHO = f"echo {ARG_ECHO}"


class EchoBot(Plugin):
    async def start(self) -> None:
        self.set_command_spec(CommandSpec(
            commands=[Command(
                syntax=COMMAND_PING,
                description="Ping the bot",
            ), Command(
                syntax=COMMAND_ECHO,
                description="Echo something",
                arguments={
                    ARG_ECHO: Argument(matches=".+", required=True,
                                       description="The content to echo"),
                },
            )],
        ))
        self.client.add_command_handler(COMMAND_PING, self.ping_handler)
        self.client.add_command_handler(COMMAND_ECHO, self.echo_handler)

    async def stop(self) -> None:
        self.client.remove_command_handler(COMMAND_PING, self.ping_handler)
        self.client.remove_command_handler(COMMAND_ECHO, self.echo_handler)

    @staticmethod
    def time_since(ms: int) -> str:
        diff = int(time() * 1000) - ms
        if abs(diff) < 10 * 1_000:
            return f"{diff} ms"
        elif abs(diff) < 60 * 1_000:
            return f"{round(diff / 1_000, 1)} seconds"
        minutes, seconds = divmod(diff / 1_000, 60)
        if abs(minutes) < 60:
            return f"{minutes} minutes and {seconds} seconds"
        hours, minutes = divmod(minutes, 60)
        if abs(hours) < 24:
            return f"{hours} hours, {minutes} minutes and {seconds} seconds"
        days, hours = divmod(hours, 24)
        return f"{days} days, {hours} hours, {minutes} minutes and {seconds} seconds"

    async def ping_handler(self, evt: MessageEvent) -> None:
        await evt.reply(f"Pong! (ping took {self.time_since(evt.timestamp)} to arrive)")

    @staticmethod
    async def echo_handler(evt: MessageEvent) -> None:
        await evt.respond(evt.content.command.arguments[ARG_ECHO])
