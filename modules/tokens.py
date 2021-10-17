from discord.ext.commands import Cog, Bot, command, Context
from discord import Client, Status
from bot_api import _m_s


class Login(Client):
    async def on_connect(self):
        await self.close()


class Tokens(Cog):
    def __init__(self, bot: Bot):
        self.bot = bot

    @command(aliases=['checktoken', 'ct'])
    async def trytoken(self, ctx: Context, *, token: str):
        try:
            await Login(status=Status.offline).login(token)
        except Exception as e:
            await ctx.reply(f'Token is invalid! ```{e} ```')
        else:
            await ctx.reply('Token is valid!')


def setup(bot: Bot):
    bot.add_cog(Tokens(bot))
    _m_s(__file__)
