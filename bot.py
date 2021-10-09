from discord.ext.commands import Bot, CommandNotFound
from bot_api import Log


class Bot(Bot):
    async def on_command(self, ctx):
        Log.log(f'Used command {ctx.message.content}', 'LOG')

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
