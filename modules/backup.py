from discord.ext.commands import Cog, Bot, command, Context
from bot_api import _m_s
from zipfile import ZipFile
from os import walk
from os.path import basename
from os import chdir


class Backup(Cog):
    def __init__(self, bot: Bot):
        self.bot = bot

    @Cog.listener()
    async def on_connect(self):
        chdir('backups')
        with ZipFile(f'backup {self.bot.started.day}-{self.bot.started.month}-{self.bot.started.year} {self.bot.started.hour}:{self.bot.started.minute}:{self.bot.started.second}.zip') as f:
            for n, sf, m in walk('.'):
                for nm in m:
                    f.write(join(n, nm), basename(join(n, nm)))
        chdir('..')


def setup(bot: Bot):
    bot.add_cog(Backup(bot))
    _m_s(__file__)
