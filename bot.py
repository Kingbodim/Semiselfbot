from discord.ext.commands import Bot
from bot_api import Log


class Bot(Bot):
    async def on_command(self, ctx):
        Log.log(f'Used command {ctx.message.content}')

     async def on_command_error(ctx, e):
         await ctx.reply(f'❌ Error: ```{e} ```')
