from discord.ext.commands import Cog, Bot, command, Context
from bot_api import _m_s
from asyncio import create_subprocess_shell
from asyncio.subprocess import PIPE, STDOUT


class Git(Cog):
    def __init__(self, bot: Bot):
        self.bot = bot


    @command(aliases=['push'])
    async def gitpush(self, ctx: Context):
        p = await create_subprocess_shell('bash push.sh', stdout=PIPE, stderr=STDOUT)
        await ctx.reply(f'```{(await p.communicate())[0].decode()}```')

    @command(aliases=['pull', 'update'])
    async def gitpull(self, ctx: Context):
        p = await create_subprocess_shell('bash pull.sh', stdout=PIPE, stderr=STDOUT)
        await ctx.reply(f'```{(await p.communicate())[0].decode()}```')


def setup(bot: Bot):
    bot.add_cog(Git(bot))
    _m_s(__file__)
