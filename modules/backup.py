from discord.ext.commands import Cog, Bot, Context, command
from discord import File
from bot_api import _m_s, Log
from shutil import make_archive
from os import remove


class Backup(Cog):
    def __init__(self, bot: Bot):
        self.bot = bot

    @Cog.listener()
    async def on_connect(self):
        #make_archive(f'backups/backup {self.bot.started.day}-{self.bot.started.month}-{self.bot.started.year} {self.bot.started.hour}:{self.bot.started.minute}:{self.bot.started.second}', 'zip', '.')
        Log.log(f'Sucessfully backed up the whole bot! (File "backups/backup {self.bot.started.day}-{self.bot.started.month}-{self.bot.started.year} {self.bot.started.hour}:{self.bot.started.minute}:{self.bot.started.second}.zip")')

    @command(aliasses=['getbotcode'])
    async def getbot(self, ctx: Context):
        make_archive('Selfbot', 'zip', '.')
        await ctx.reply(file=File('Selfbot.zip'))
        remove('Selfbot.zip')

    @command(aliasses=['backup'])
    async def save(self, ctx: Context):
        make_archive(f'backups/backup {self.bot.started.day}-{self.bot.started.month}-{self.bot.started.year} {self.bot.started.hour}:{self.bot.started.minute}:{self.bot.started.second}', 'zip', '.')
        await ctx.reply('Done!')


def setup(bot: Bot):
    bot.add_cog(Backup(bot))
    _m_s(__file__)
