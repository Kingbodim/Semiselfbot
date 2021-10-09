from discord.ext.commands import Cog, Bot, group, Context
from bot_api import _m_s
from aiofiles import open as aopen


class Snippets(Cog):
    def __init__(self, bot: Bot):
        self.bot = bot

    @group()
    async def snippet(self, ctx: Context):
        if ctx.invoked_subcommand is None:
            await ctx.reply(f'Invalid command! Usage: `{ctx.prefix}snippet <command>`')

    @snippet.command(aliases=['see'])
    async def show(self, ctx: Context, *, name):
        async with aopen(f'snippets/{name}.txt', 'r') as f:
            await ctx.reply(await f.read())

    @snippet.command(aliases=['set'])
    async def save(self, ctx: Context, name, *, content):
        async with aopen(f'snippets/{name}.txt', 'w') as f:
            await f.write(content)
            await ctx.reply(f'Sucessfully saved `{name}` snippet')


def setup(bot: Bot):
    bot.add_cog(Snippets(bot))
    _m_s(__file__)
