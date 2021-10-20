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

    @command(aliases=['rawbytes', 'getrawbytes', 'bytes'])
    async def getrawcontentbytes(self, ctx: Context, msg: Message = None):
        if msg is not None:
            await ctx.reply(f'```{msg.content.encode()}```')
        elif ctx.message.reference:
            await ctx.reply(f'```{(await ctx.fetch_message(ctx.message.reference.message_id)).content.encode()}```')

    @command(aliases=['ge', 'embedcontent', 'getem'])
    async def getembed(self, ctx: Context, msg: Message = None):
        if msg is not None:
            await ctx.reply(f'```json\n{dumps(msg.embeds[0].to_dict(), indent=4)}```')
        elif ctx.message.reference:
            await ctx.reply(f'```json\n{dumps((await ctx.fetch_message(ctx.message.reference.message_id)).embeds[0].to_dict(), indent=4)}```')

    @command(aliases=['msg', 'duplicate', 'resend'])
    async def getmsg(self, ctx: Context, msg: int = None, channel: int = None):
        if channel:
            msg = await self.bot.get_channel(channel).fetch_message(msg)
        elif msg:
            msg = await ctx.fetch_message(msg)
        elif ctx.message.reference:
            msg = await ctx.fetch_message(ctx.message.reference.message_id)
        else:
            return
        await ctx.reply(content=msg.content, embed=msg.embeds[0] if msg.embeds else None)


    @command(aliases=['removemessage', 'deletemsg', 'delmsg'])
    async def rmmsg(self, ctx: Context, msg: Message = None):
        if msg is not None:
            await msg.delete()
        elif ctx.message.reference:
            await (await ctx.fetch_message(ctx.message.reference.message_id)).delete()


def setup(bot: Bot):
    bot.add_cog(Raw(bot))
    _e_s(__file__)
