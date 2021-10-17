from discord.ext.commands import Cog, Bot
from discord.embeds import _EmptyEmbed
from discord import Message
from replit import db
from asyncio import sleep
from bot_api import _m_s, dump_giveaway, dump_win
from datetime import datetime
from random import randint


class GwSniper(Cog):
    def __init__(self, bot: Bot):
        self.bot = bot

    @Cog.listener()
    async def on_message(self, message: Message):
        if message.author.id == 294882584201003009 or message.author.id == 824119071556763668:
            try:
                if message.channel.permissions_for(message.guild.me).send_messages:
                    return
                if message.embeds and db['giveaway sniper']:
                    if not isinstance(message.embeds[0].author.name, _EmptyEmbed) and 'nitro' in message.embeds[0].author.name.lower() and 'GIVEAWAY' in message.content:
                        self.bot.loop.create_task(dump_giveaway(self.bot, message))
                        now = datetime.now()
                        if (message.embeds[0].timestamp-now).seconds <= 7: return
                        await sleep((message.embeds[0].timestamp-now).seconds/2)
                        await message.add_reaction('🎉')
                if message.mentions and message.mentions[0] == self.bot.user and db['giveaway claimer']:
                    await sleep(randint(5, 7))
                    h = await message.channel.history(limit=5).get(author__bot=False)
                    self.bot.loop.create_task(dump_win(self.bot, message, h))
            except:
                pass
        if message.author.id == 525748238255390721:
            if message.channel.permissions_for(message.guild.me).send_messages:
                return
            if message.embeds and db['giveaway sniper']:
                if not isinstance(message.embeds[0].title, _EmptyEmbed) and 'nitro' in message.embeds[0].title.lower():
                    await sleep(30)
                    await message.add_reaction(message.reactions[0])


def setup(bot: Bot):
    bot.add_cog(GwSniper(bot))
    _m_s(__file__)
