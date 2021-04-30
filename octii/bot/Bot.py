import inspect
import asyncio

from typing import List, Optional
from octii.api.api import APIClient
from .converters import convert_args
from octii.api.Message import Message

class Command:
    def __init__(self, func, name: str, description: str, aliases: List[str], params_data: List[inspect.Parameter]):
        self.func = func
        self.name = name
        self.description = description
        self.aliases = aliases
        self.params_data = params_data

def create_command(func, *, name: Optional[str] = None, aliases: Optional[List[str]] = None):
    return Command(func, name or func.__name__, func.__doc__ or "No description.", aliases or [], list(inspect.signature(func).parameters.values()))

class Bot:
    def __init__(self, token: str, prefix: str = "!"):
        self._commands = {
            'help': create_command(self.default_help_command, name="help", aliases=['cmds', 'cmd', 'manual'])
        }
        self._api_client = APIClient()
        self._api_client.set_auth_token(token)
        self.prefix = prefix
        self.selfbot = False

    async def default_help_command(self, ctx):
        """The default octii.py help command. Prints out a list of every command and their descriptions."""
        text = "```\n"

        for command in self._commands.values():
            text += command.name + ": " + command.description + "\n"

        ctx.send(text + "```")

    def run(self):
        def handle_message(msg_data):
            if not self.selfbot or msg_data['author']['id'] == self._api_client.user_id:
                if msg_data['content'].startswith(self.prefix):
                    args = msg_data['content'].split(' ')
                    cmd_name = args[0]
                    args = args[1:]

                    try:
                        cmd = self._commands[cmd_name[len(self.prefix):]]
                        asyncio.create_task(cmd.func(create_context_for_message(self, msg_data), *convert_args(cmd.func, self, cmd.params_data, *args)))
                    except KeyError:
                        raise
                        print("Command does not exist!", cmd_name)
                    except Exception as e:
                        raise

        self._api_client.init_sse()
        self._api_client.sse.on_message += handle_message
        self._api_client.run()

    def add_command(self, command):
        self._commands[command.name] = command

    def command(self, *args, **kwargs):
        def decorator(func):
            result = create_command(func, *args, **kwargs)
            self.add_command(result)
            return result

        return decorator

class Context:
    def __init__(self, bot: Bot, msg: Message):
        self._bot = bot
        self.msg = msg
        self.channel_id = ""

    def send(self, msg: str):
        return self._bot._api_client.send_message(self.channel_id, msg)

def create_context_for_message(bot, msg_data):
    ctx = Context(bot, Message.load_json(msg_data))
    ctx._bot = bot
    ctx.channel_id = msg_data['channel_id']
    ctx.author = bot._api_client.fetch_user(msg_data['author']['id'])
    return ctx