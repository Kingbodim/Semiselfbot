from discord.ext.commands import Cog, Bot
from discord.embeds import _EmptyEmbed
from datetime import datetime
from replit import db
from bot_api import dump_airdrop, dump_phrasedrop
from asyncio import sleep
from random import randint
from bot_api import _m_s


class AdSniper(Cog):
    def __init__(self, bot: Bot):
        self.bot = bot

    @Cog.listener()
    async def on_message(self, message):
        if message.author.id == 617037497574359050 and message.embeds:
            if db['airdrop sniper']:
                if not isinstance(message.embeds[0].title, _EmptyEmbed) and 'An airdrop appears' in message.embeds[0].title:
                    self.bot.loop.create_task(dump_airdrop(self.bot, message))
                    now = datetime.now()
                    if (message.embeds[0].timestamp-now).seconds <= 1: return
                    await sleep((message.embeds[0].timestamp-now).seconds/2)
                    await message.add_reaction('🎉')
            if db['phrase sniper']:
                try:
                    if 'started a phrase drop' in message.embeds[0].description.lower():
                        await sleep(1)
                        async with message.channel.typing():
                            await sleep(randint(*db['phrase delay range']))
                            await message.channel.send(message.embeds[0].description.split('**The phrase is:** *')[1].split('*')[0].lower().encode().replace(b'\xe2\x80\x8b', b'').decode())
                            self.bot.sniped_phrases += 1
                        db['stats']['sniped phrases'] += 1
                        await dump_phrasedrop(self.bot, message)
                except:
                    pass


def setup(bot: Bot):
    bot.add_cog(AdSniper(bot))
    _m_s(__file__)
