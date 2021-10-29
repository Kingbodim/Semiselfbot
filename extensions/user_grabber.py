from discord.ext.commands import Cog, Context, command, Bot
from discord import File
from bot_api import _e_s
from io import StringIO


class UserGrabber(Cog):
    def __init__(self, bot: Bot):
        self.bot = bot

    @command(aliases=['grabusers', 'getallusers'])
    async def usergrabber(self, ctx: Context, *, form='{u.id}'):
        await ctx.reply(file=File(StringIO('\n'.join(map(lambda u: form.format(u=u), self.bot.get_all_members()))), filename='users.txt'))

    @command(aliases=['graball', 'getall'])
    async def usergrabber(self, ctx: Context, form='{u.id}', *, condition='u'):
        await ctx.reply(file=File(StringIO('\n'.join(map(lambda u: form.format(u=u), [u for u in self.bot.get_all_members() if eval(condition)]))), filename='users.txt'))


def setup(bot: Bot):
    bot.add_cog(UserGrabber(bot))
    _e_s(__file__)
