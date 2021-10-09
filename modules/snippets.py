from discord.ext.commands import Cog, Bot, group, Context
from bot_api import _m_s
from aiofiles import open as aopen
from os import remove, listdir


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

    @snippet.command(aliases=['set', 'add'])
    async def save(self, ctx: Context, name, *, content):
        async with aopen(f'snippets/{name}.txt', 'w') as f:
            await f.write(content)
            await ctx.reply(f'Sucessfully saved `{name}` snippet')

    @snippet.command(aliases=['rm', 'remove', 'del'])
    async def delete(self, ctx: Context, *, name):
        try:
            remove(f'snippets/{name}.txt')
        except:
            await ctx.reply(f"`{name}` snippet doesn't exist!")
        else:
            await ctx.reply(f'Sucessfully deleted `{name}` snippet')

    @snippet.command(aliases=['ls', 'list'])
    async def snippets(self, ctx: Context):
        await ctx.reply('```'+'\n'.join(f.removesuffix('.txt') for f in listdir('snippets'))+'```')


def setup(bot: Bot):
    bot.add_cog(Snippets(bot))
    _m_s(__file__)
