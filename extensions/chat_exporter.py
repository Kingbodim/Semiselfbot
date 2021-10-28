from discord.ext.commands import Cog, Context, command, Bot
from discord import File
from bot_api import _e_s
from io import StringIO


class ChannelExporter(Cog):
    def __init__(self, bot: Bot):
        self.bot = bot

    @command(aliases=['exportchannel'])
    async def export_channel(self, ctx: Context, cid: int = None, *, form='[ {message.author.name} ] {message.content}'):
        out = ''
        async for message in self.bot.get_channel(cid or ctx.channel.id).history(limit=100, oldest_first=True):
            out += form.format(message=message, m=message) + '\n'
        await ctx.send(file=File(fp=StringIO(out), filename='Messages.txt'))

    @command(aliases=['exportdm'])
    async def export_dm(self, ctx: Context, cid: int = None, *, form='[ {message.author.name} ] {message.content}'):
        out = ''
        async for message in self.bot.get_user(cid or ctx.channel.id).history(limit=100, oldest_first=True):
            out += form.format(message=message, m=message) + '\n'
        await ctx.send(file=File(fp=StringIO(out), filename='Messages.txt'))


def setup(bot: Bot):
    bot.add_cog(ChannelExporter(bot))
    _e_s(__file__)
