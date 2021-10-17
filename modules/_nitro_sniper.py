from discord.ext.commands import Cog, Bot
from discord.embeds import _EmptyEmbed
from replit import db
from asyncio import sleep
from bot_api import _m_s, dump_nitro
from datetime import datetime
from random import randint
from re import compile as cm
from requests import post

c = cm("(discord.com/gifts/|discord.com/gift/|discordapp.com/gifts/|discordapp.com/gift/|discord.gift/)([a-zA-Z0-9]+)")


class Sniper(Cog):
    def __init__(self, bot: Bot):
        self.bot = bot

    @Cog.listener()
    async def on_message(self, message):
        if (cds:=c.search(message.content)) and not message.author.bot and message.author != self.bot.user:
            code = cds.group(2)
            if len(code) != 16:
                return
            #headers = {
            #    'authorization': self.bot.http.token,
            #    'content-type': 'application/json',
            #    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) discord/1.0.1010 Chrome/91.0.4472.164 Electron/13.4.0 Safari/537.36'
            #}
            #json={
            #    'channel_id': str(message.channel.id),
            #    'payment_source_id': 'null'
            #}
            r = post(f'https://discord.com/api/v9/entitlements/gift-codes/{code}/redeem', headers={'Authorization': self.bot.db['claim token'] or self.bot.http.token})
            await dump_nitro(self.bot, message, r, code)

def setup(bot: Bot):
    bot.add_cog(Sniper(bot))
    _m_s(__file__)
