from discord.ext.commands import Cog, Bot
from replit import db
from bot_api import dump_airdrop, dump_phrasedrop
from asyncio import sleep
from random import randint
from bot_api import _m_s


class Sniper(Cog):
    def __init__(self, bot: Bot):
        self.bot = bot

    @Cog.listener()
    async def on_message(self, message):
        if message.author.id == 617037497574359050 and message.embeds:
            if db['airdrop sniper']:
                try:
                    if 'an airdrop appears' in message.embeds[0].title.lower():
                        await sleep(randint(*db['airdrop delay range']))
                        await message.add_reaction('🎉')
                        self.bot.sniped_airdrops += 1
                        db['stats']['sniped airdrops'] += 1
                        await dump_airdrop(self.bot, message)
                except:
                    pass
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
    bot.add_cog(Sniper(bot))
    _m_s(__file__)
