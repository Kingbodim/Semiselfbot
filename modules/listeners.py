from discord.ext.commands import Cog, Bot
from bot_api import _m_s, Log


class Listeners(Cog):
    def __init__(self, bot: Bot):
        self.bot = bot

    @Cog.listener()
    async def on_connect(self):
        Log.log(f'Bot connected as {self.bot.user}')

    @Cog.listener()
    async def on_ready(self):
        Log.log(f'Bot ready as {self.bot.user}')

    @Cog.listener()
    async def on_message_edit(self, before, after):
        await self.bot.process_commands(after)


def setup(bot: Bot):
    bot.add_cog(Listeners(bot))
    _m_s(__file__)
