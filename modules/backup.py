from discord.ext.commands import Cog, Bot, command, Context
from bot_api import _m_s
from shutil import make_archive
from os import walk
from os.path import basename
from os import chdir


class Backup(Cog):
    def __init__(self, bot: Bot):
        self.bot = bot

    @Cog.listener()
    async def on_connect(self):
        make_archive(f'backups/backup {self.bot.started.day}-{self.bot.started.month}-{self.bot.started.year} {self.bot.started.hour}:{self.bot.started.minute}:{self.bot.started.second}.zip', 'zip', '.')


def setup(bot: Bot):
    bot.add_cog(Backup(bot))
    _m_s(__file__)
