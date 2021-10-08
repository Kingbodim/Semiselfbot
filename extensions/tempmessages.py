from discord.ext.commands import Cog, Context, command, Bot
from bot_api import _e_s
from asyncio import sleep


class TempMessages(Cog):
    def __init__(self, bot: Bot):
        self.bot = bot

    @command(aliases=['tempmessage', 'autodel', 'autodelete', 'ad'])
    async def tmpmsg(self, ctx: Context, delay: int, *, message):
        await ctx.message.delete()
        m = await ctx.send(message, delete_after=delay)


def setup(bot: Bot):
    bot.add_cog(TempMessages(bot))
    _e_s(__file__)
