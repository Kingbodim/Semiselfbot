from discord.ext.commands import Bot, CommandNotFound, MinimalHelpCommand
from discord import Embed
from bot_api import Log, prefix, ka, load_modules, load_extensions
from os import environ
from discord import Status
from replit import db
from datetime import datetime


class Help(MinimalHelpCommand):
    async def send_pages(self):
        destination = self.get_destination()
        for p in self.paginator.pages:
            e = Embed(description=p)
            await destination.send(embed=e)


class Bot(Bot):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, status=Status.offline, self_bot=True, case_insensitive=True, strip_after_prefix=True, command_prefix=prefix(), max_messages=10000, **kwargs)
        ka()
        self.db = db
        self.started = datetime.utcnow()
        self.sniped_airdrops = 0
        self.sniped_phrases = 0
        load_modules(self)
        load_extensions(self)
        with open('uptime register.txt', 'a') as f:
            f.write(str(self.started) + '\n')
        self.run(environ['TOKEN'])

    async def on_command(self, ctx):
        Log.log(f'Used command {ctx.message.content}')

    async def on_command_error(self, ctx, e):
        if isinstance(e, CommandNotFound):
            return
        await ctx.reply(f'❌ Error: ```{e} ```')

    async def on_connect(self):
        Log.log(f'Bot connected as {self.user}')

    async def on_ready(self):
        Log.log(f'Bot ready as {self.user}')

    async def on_message_edit(self, before, after):
        await self.process_commands(after)
