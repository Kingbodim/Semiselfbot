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

im_setup = {
    ';h': 5*60,
    ';f': 5*60,
    ';s': 10,
    ';up p a': 10,
    ';up b a': 60,
    ';ca': 60*60,
    ';rb': 60
}


async def repeat(channel, cmd, delay):
    while True:
        await channel.send(cmd)
        await sleep(randint(delay+1, delay+2))


async def cmds(bot, channel, setup):
    return [bot.loop.create_task(repeat(channel, cmd, delay)) for cmd, delay in setup.items()]


class Bots(Cog):
    def __init__(self, bot: Bot):
        self.bot = bot
        self.tasks = {
            'dank': None,
            'im': None
            }

    @group(invoke_without_command=True, aliases=['automate', 'autoplay'])
    async def play(self, ctx: Context):
        await ctx.reply(f'Invalid command passed. Usage: `{ctx.prefix}{ctx.command} <bot> <options>`, ex. `{ctx.prefix}{ctx.command} dank start`')

    @play.command(aliases=['play'])
    async def start(self, ctx: Context):
        await ctx.invoke(self.start1)
        await ctx.invoke(self.start2)

    @play.command(aliases=['cancel'])
    async def stop(self, ctx: Context):
        await ctx.invoke(self.stop1)
        await ctx.invoke(self.stop2)

    @play.group(invoke_without_command=True, aliases=['memer'])
    async def dank(self, ctx: Context):
        await ctx.reply(f'Invalid command passed. Usage: `{ctx.prefix}{ctx.command} <options>`, ex. `{ctx.prefix}{ctx.command} start`')

    @dank.command(name='start', aliases=['play'])
    async def start1(self, ctx: Context, channel_id: int = 896480965222875137):
        self.tasks['dank'] = await cmds(self.bot, await self.bot.fetch_channel(channel_id), dank_setup)

    @dank.command(name='stop', aliases=['cancel'])
    async def stop1(self, ctx: Context):
        [t.cancel() for t in self.tasks['dank']]

    @play.group(invoke_without_command=True, aliases=['idleminer'])
    async def im(self, ctx: Context):
        await ctx.reply(f'Invalid command passed. Usage: `{ctx.prefix}{ctx.command} <options>`, ex. `{ctx.prefix}{ctx.command} start`')

    @im.command(name='start', aliases=['play'])
    async def start2(self, ctx: Context, channel_id: int = 896480981358366750):
        self.tasks['im'] = await cmds(self.bot, await self.bot.fetch_channel(channel_id), im_setup)

    @im.command(name='stop', aliases=['cancel'])
    async def stop2(self, ctx: Context):
        [t.cancel() for t in self.tasks['im']]


def setup(bot: Bot):
    bot.add_cog(Bots(bot))
    _m_s(__file__)
