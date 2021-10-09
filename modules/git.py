from discord.ext.commands import Cog, Bot, command, group, Context
from bot_api import _m_s
from asyncio import create_subprocess_shell
from asyncio.subprocess import PIPE, STDOUT


class Git(Cog):
    def __init__(self, bot: Bot):
        self.bot = bot

    @group()
    async def git(self, ctx: Context):
        if ctx.invoked_subcommand is None:
            await ctx.reply(f'Invalid git command passed. Usage: `{ctx.prefix}git <command>`, ex. `{ctx.prefix}git pull`')

    @git.command()
    async def push(self, ctx: Context):
        p = await create_subprocess_shell('bash push.sh', stdout=PIPE, stderr=STDOUT)
        await ctx.reply(f'```{(await p.communicate())[0].decode()}```')

    @git.command()
    async def pull(self, ctx: Context):
        p = await create_subprocess_shell('bash pull.sh', stdout=PIPE, stderr=STDOUT)
        await ctx.reply(f'```{(await p.communicate())[0].decode()}```')

    @command(name='pull', aliases=['update'])
    async def depr(self, ctx: Context):
        await ctx.reply(f'`{ctx.prefix}{ctx.command}` command is deprecated! Use `{ctx.prefix}git pull` instead')

def setup(bot: Bot):
    bot.add_cog(Git(bot))
    _m_s(__file__)
