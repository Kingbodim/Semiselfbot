from discord.ext.commands import Bot, CommandNotFound
from bot_api import Log


class Bot(Bot):
    async def on_command(self, ctx):
        Log.log(f'Used command {ctx.message.content}')

    async def on_command_error(self, ctx, e):
        if isinstance(e, CommandNotFound):
            return
        await ctx.reply(f'❌ Error: ```{e} ```')
