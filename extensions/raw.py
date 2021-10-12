from discord.ext.commands import Cog, Context, command, Bot
from discord import Message
from bot_api import _e_s
from json import dumps


class Raw(Cog):
    def __init__(self, bot: Bot):
        self.bot = bot

    @command(aliases=['raw', 'getraw', 'getcontent'])
    async def getrawcontent(self, ctx: Context, msg: Message = None):
        if msg is not None:
            await ctx.reply(f'```{msg.content}```')
        elif ctx.message.reference:
            await ctx.reply(f'```{(await ctx.fetch_message(ctx.message.reference.message_id)).content}```')

    @command(aliases=['ge', 'embedcontent', 'getem'])
    async def getembed(self, ctx: Context, msg: Message = None):
        if msg is not None:
            await ctx.reply(f'```json\n{dumps(msg.embeds[0].to_dict(), indent=4)}```')
        elif ctx.message.reference:
            await ctx.reply(f'```json\n{dumps((await ctx.fetch_message(ctx.message.reference.message_id)).embeds[0].to_dict(), indent=4)}```')


def setup(bot: Bot):
    bot.add_cog(Raw(bot))
    _e_s(__file__)
