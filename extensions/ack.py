from discord.ext.commands import Cog, Context, command, Bot
from bot_api import _e_s


class Ack(Cog):
    def __init__(self, bot: Bot):
        self.bot = bot

    @command(aliases=[''])
    async def test(self, ctx: Context):
        pass


def setup(bot: Bot):
    bot.add_cog(Ack(bot))
    _e_s(__file__)
