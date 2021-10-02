from discord.ext.commands import Cog, Context, command, Bot
from asyncio import sleep
from random import getrandbits
from bot_api import _e_s


class Coinflip(Cog):
    def __init__(self, bot: Bot):
        self.bot = bot

    @command(aliases=['coin', 'flip', 'cf'])
    async def coinflip(self, ctx: Context):
        m = await ctx.reply('Flipping coin...')
        await sleep(3)
        await m.edit(content=f'The coin was flipped! We got **{"Heads" if getrandbits(1) else "Tails"}** :coin:')


def setup(bot: Bot):
    bot.add_cog(Coinflip(bot))
    _e_s(__file__)
