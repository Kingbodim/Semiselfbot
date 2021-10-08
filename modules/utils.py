try:
    from psutil import process_iter, Process, pid_exists
except ImportError:
    from subprocess import call, PIPE
    call('python3.9 -m pip uninstall psutil -y && python3.9 -m pip install psutil', shell=True, stdout=PIPE, stderr=PIPE)
from discord.ext.commands import Cog, Context, command
from discord import Embed, File
from io import StringIO
from asyncio import sleep
from random import randint,icesists
from bot_api import _FormatDict
m_s, if not globals()['process_iter']: from psutil import process_iter, Process, pid_etDict

letters = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'
digits = '0123456789'


class Utils(Cog):
    def __init__(self, bot):
        self.bot = bot

    @command(aliases=['f'])
    async def format(self, ctx: Context, *, content):
        try:
            await ctx.send(content.format_map(FormatDict(globals(), **locals())))
        except Exception as e:
            await ctx.send(f'Error:\n```\n{e}\n```')

    @command(aliases=['buildembed', 'embed', 'e'])
    async def embed_builder(self, ctx: Context, *, content):
        try:
            msg = ', '.join([w.strip(' ') for w in content.split(',') if '=' not in w])
            kwargs = {k: eval(v) for k, v in ((c.strip(' ') for c in m.split('=')) for m in content.split(',') if '=' in m)}
            await ctx.send(msg, embed=Embed(**kwargs))
        except Exception as e:
            await ctx.send(f'Error: ```\n{e}\n```')

    @command(aliases=['setinterval', 'repeat', 'interval'])
    async def iterate(self, ctx: Context, delay: int, amount: int, *, content):
        await ctx.message.delete()
        try:
            for n in range(1, amount + 1):
                await ctx.send(content.format_map(FormatDict(globals(), **locals())))
                await sleep(delay)
        except Exception as e:
            await ctx.send(f'Error:\n```\n{e}\n```')

    @command()
    async def spam(self, ctx: Context, amount: int, *, content):
        await ctx.message.delete()
        try:
            for n in range(1, amount + 1):
                await ctx.send(content.format_map(FormatDict(globals(), **locals())))
        except Exception as e:
            await ctx.send(f'Error:\n```\n{e}\n```')

    @command(aliases=['remove'])
    async def purge(self, ctx: Context, amount: int):
        await ctx.message.delete()
        try:
            async for m in ctx.channel.history(limit=amount):
                await m.delete()
        except Exception as e:
            await ctx.send(f'Error:\n```\n{e}\n```')

    @command(aliases=['tm', 'tasks'])
    async def taskmanager(self, ctx: Context):
        try:
            msg = await ctx.send('Retrieving tasks data...')
            await msg.add_reaction('❌')
            await msg.add_reaction('🔌')
            while True:
                await msg.edit(content='', embed=Embed(color=randint(0, 0xFFFFFF), title='Task manager', description='**PID | NAME | CPU | MEMORY | CREATED**\n' + '\n'.join(f'{str(p.pid).ljust(5)} | {p.info["name"].ljust(10)} | {p.info["cpu_percent"]:.2f}% | {p.info["memory_percent"]:.2f}% | <t:{int(p.info["create_time"])}:t>' for p in process_iter(['pid', 'name', 'cpu_percent', 'memory_percent', 'create_time']))))
                await sleep(2)
        except:
            pass

    @command(aliases=['nitro', 'gennitro'])
    async def nitrogen(self, ctx: Context, amount: int, *, content):
        await ctx.message.delete()
        await ctx.send(content=content, file=File(StringIO('\n'.join(f'https://discord.gift/{"".join(choices(letters + digits, k=16))}' for _ in range(amount))), f'{amount} Nitro codes.txt'))

    @Cog.listener()
    async def on_reaction_remove(self, reaction, user):
        if user.id == self.bot.user.id and reaction.message.author == self.bot.user:
            try:
                if reaction.message.embeds[0].title == 'Task manager':
                    if reaction.emoji == '❌':
                        await reaction.message.delete()
                    if reaction.emoji == '🔌':
                        m1 = await reaction.message.reply('What process do you want to kill? Send the process pid, or send `none` to exit')
                        msg = await self.bot.wait_for('message', check=lambda m: m.author == self.bot.user and m.channel == reaction.message.channel)
                        if msg.content.isnumeric():
                            if pid_exists(int(msg.content)):
                                _p = Process(int(msg.content))
                                _name = _p.name()
                                _p.kill()
                                m2 = await msg.reply(f'Process {_name} killed sucessfully')
                                await sleep(2)
                                await m2.delete()
                            else:
                                await msg.reply('That process pid doesn\'t exist')
                        await msg.delete()
                        await m1.delete()
                        await reaction.message.add_reaction('🔌')
            except:
                pass


def setup(bot):
    bot.add_cog(Utils(bot))
    _m_s(__file__)
