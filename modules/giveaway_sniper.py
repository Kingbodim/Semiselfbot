from discord.ext.commands import Cog, Bot
from discord.embeds import _EmptyEmbed
from replit import db
from asyncio import sleep
from bot_api import _m_s, dump_giveaway, dump_win
from datetime import datetime
from random import randint


class GwSniper(Cog):
    def __init__(self, bot: Bot):
        self.bot = bot

    @Cog.listener()
    async def on_message(self, message):
        if message.author.id == 294882584201003009:
            try:
                if message.embeds and db['giveaway sniper']:
                    if not isinstance(message.embeds[0].author.name, _EmptyEmbed) and 'nitro' in message.embeds[0].author.name.lower() and '**GIVEAWAY**' in message.content:
                        self.bot.loop.create_task(dump_giveaway(self.bot, message))
                        now = datetime.now()
                        if (message.embeds[0].timestamp-now).seconds <= 7: return
                        await sleep((message.embeds[0].timestamp-now).seconds/2)
                        await message.add_reaction('🎉')
                if message.mentions and message.mentions[0] == self.bot.user and db['giveaway claimer']:
                    await sleep(randint(5, 7))
                    mg = [m.author async for m in message.channel.history(limit=3) if not m.author.bot]
                    self.bot.loop.create_task(dump_win(self.bot, message, mg))
                    for m in mg:
                        try:
                            await m.send('claim')
                        except:
                            pass
            except:
                pass

def setup(bot: Bot):
    bot.add_cog(GwSniper(bot))
    _m_s(__file__)
