from discord.ext.commands import Cog, Context, command, Bot
from bot_api import _e_s


class Raw(Cog):
    def __init__(self, bot: Bot):
        self.bot = bot

    @command(aliases=['raw', 'getraw', 'getcontent'])
    async def getrawcontent(self, ctx: Context):
        if ctx.message.reference:
            await ctx.reply(f'```{(await ctx.fetch_message(ctx.message.reference.message_id)).content}```')


def setup(bot: Bot):
    bot.add_cog(Raw(bot))
    _e_s(__file__)
