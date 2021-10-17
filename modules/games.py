from discord.ext.commands import Cog, Bot, command, Context
from bot_api import _m_s
from asyncio import sleep
import string


class Games(Cog):
    def __init__(self, bot: Bot):
        self.bot = bot

    @command(aliases=['alphabet', 'abecedary'])
    async def abc(self, ctx: Context):
        for l in string.ascii_lowercase:
            await ctx.message.edit(content=l)
            await sleep(0.5)


def setup(bot: Bot):
    bot.add_cog(Games(bot))
    _m_s(__file__)
