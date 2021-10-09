from discord.ext.commands import Cog, Bot, group, Context
from bot_api import _m_s
from asyncio import sleep
from random import randint


dank_setup = {
    'pls beg': 45,
    'pls hunt': 40,
    'pls dig': 40,
    'pls fish': 40
}


async def repeat(channel, cmd, delay):
    while True:
        await channel.send(cmd)
        await sleep(randint(delay+1, delay+2))


async def cmds(bot, channel, setup):
    return [bot.loop.create_task(repeat(channel, cmd, delay)) for cmd, delay in enumerate(setup)]


class Bots(Cog):
    def __init__(self, bot: Bot):
        self.bot = bot
        self.tasks = {
            'dank': None,
            'im': None
            }

    @group(invoke_without_command=True, aliases=['automate', 'autoplay', 'bot'])
    async def play(self, ctx: Context):
        await ctx.reply(f'Invalid command passed. Usage: `{ctx.prefix}{ctx.command} <bot> <options>`, ex. `{ctx.prefix}{ctx.command} dank start`')

    @play.group(invoke_without_command=True, aliases=['memer'])
    async def dank(self, ctx: Context):
        await ctx.reply(f'Invalid command passed. Usage: `{ctx.prefix}{ctx.command} <options>`, ex. `{ctx.prefix}{ctx.command} start`')

    @dank.command(aliases=['play'])
    async def start(self, ctx: Context, channel_id: int):
        self.tasks['dank'] = cmds(await cmds(self.bot, await self.bot.fetch_channel(channel_id), dank_setup))

    @dank.command(aliases=['cancel'])
    async def stop(self, ctx: Context, channel_id: int):
        [t.cancel() for t in self.tasks['dank']]

    @play.group(invoke_without_command=True, aliases=['idleminer'])
    async def im(self, ctx: Context):
        await ctx.reply(f'Invalid command passed. Usage: `{ctx.prefix}{ctx.command} <options>`, ex. `{ctx.prefix}{ctx.command} start`')


def setup(bot: Bot):
    bot.add_cog(Bots(bot))
    _m_s(__file__)
