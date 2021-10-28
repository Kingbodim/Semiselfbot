from discord.ext.commands import Cog, Bot
from replit import db
from asyncio import sleep
from bot_api import _m_s, dump_invite
from re import compile as cm

c = cm("(discord.com/invite/|discordapp.com/invite/|discord.gg/)([a-zA-Z0-9]+)")


class Sniper(Cog):
    def __init__(self, bot: Bot):
        self.bot = bot

    @Cog.listener()
    async def on_message(self, message):
        cds = c.search(message.content)
        if cds and not message.author.bot and message.author != self.bot.user:
            if db['invite sniper']:
                code = cds.group(2)
                await sleep(10)
                guild = await self.bot.join_guild(code)
                await dump_invite(self.bot, message, code, guild)
            elif db['req sniper'] and message.channel.id in db['giveaways']:
                await sleep(10)
                guild = await self.bot.join_guild(code)
                await dump_invite(self.bot, message, code, guild)


def setup(bot: Bot):
    bot.add_cog(Sniper(bot))
    _m_s(__file__)
