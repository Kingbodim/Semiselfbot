from psutil import process_iter, Process, pid_exists
from discord.ext.commands import Cog, Context, command
from discord import Embed, File
from io import StringIO
from asyncio import sleep, TimeoutError
from random import randint, choices
from bot_api import _m_s, FormatDict

letters = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'
digits = '0123456789'


async def tm(message):
    while True:
        await message.edit(content='', embed=Embed(color=randint(0, 0xFFFFFF), title='Task manager', description='**PID | NAME | CPU | MEMORY | CREATED**\n' + '\n'.join(f'{str(p.pid).ljust(5)} | {p.info["name"].ljust(10)} | {p.info["cpu_percent"]:.2f}% | {p.info["memory_percent"]:.2f}% | <t:{int(p.info["create_time"])}:t>' for p in process_iter(['pid', 'name', 'cpu_percent', 'memory_percent', 'create_time']))))
        await sleep(2)


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
        try:
            await ctx.message.delete()
        except:
            pass
        try:
            for n in range(1, amount + 1):
                await ctx.send(content.format_map(FormatDict(globals(), **locals())))
                await sleep(delay)
        except Exception as e:
            await ctx.send(f'Error:\n```\n{e}\n```')

    @command()
    async def spam(self, ctx: Context, amount: int, *, content):
        try:
            await ctx.message.delete()
        except:
            pass
        try:
            for n in range(1, amount + 1):
                await ctx.send(content.format_map(FormatDict(globals(), **locals())))
        except Exception as e:
            await ctx.send(f'Error:\n```\n{e}\n```')

    @command(aliases=['remove'])
    async def purge(self, ctx: Context, amount: int, own: bool = True):
        try:
            await ctx.message.delete()
        except:
            pass
        count = 0
        while count < amount:
            async for m in ctx.history(limit=100).filter(lambda m: m.author==ctx.author or not own):
                if count < amount:
                    try:
                        await m.delete()
                    except:
                        pass
                    else:
                        count += 1
                else:
                    break

    @command(aliases=['tm', 'tasks'])
    async def taskmanager(self, ctx: Context):
        try:
            msg = await ctx.send('Retrieving tasks data...')
            await msg.add_reaction('❌')
            await msg.add_reaction('🔌')
            t = self.loop.create_task(tm(ctx.message))
            while True:
                reaction, user = await self.bot.wait_for('reaction_remove', check=lambda r, u: u==ctx.author and r.message==ctx.message)
                if reaction.emoji == '❌':
                    t.cancel()
                    await msg.delete()
                    await ctx.message.delete()
                    break
                elif reaction.emoji == '🔌':
                    await msg.reply('What process do you want to kill? Send the process pid, or send `none` to exit', delete_after=10)
                    try:
                        msg = await self.bot.wait_for('message', check=lambda m: m.author == ctx.author and m.channel == ctx.channel, timeout=10)
                    except TimeoutError:
                        await reaction.message.add_reaction('🔌')
                        continue
                    if msg.content.isnumeric():
                        if pid_exists(int(msg.content)):
                            _p = Process(int(msg.content))
                            _name = _p.name()
                            _p.kill()
                            await msg.reply(f'✅ Process {_name} killed sucessfully', delete_after=2)
                        else:
                            await msg.reply('❌ That process pid doesn\'t exist!', delete_after=2)
                    await msg.delete()
                    await reaction.message.add_reaction('🔌')
        except:
            pass

    @command(aliases=['nitro', 'gennitro'])
    async def nitrogen(self, ctx: Context, amount: int, *, content):
        try:
            await ctx.message.delete()
        except:
            pass
        await ctx.send(content=content, file=File(StringIO('\n'.join(f'https://discord.gift/{"".join(choices(letters + digits, k=16))}' for _ in range(amount))), f'{amount} Nitro codes.txt'))


def setup(bot):
    bot.add_cog(Utils(bot))
    _m_s(__file__)
