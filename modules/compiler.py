from discord.ext.commands import command, Cog, Context, Bot
from asyncio import create_subprocess_exec as Popen, create_subprocess_shell as Sopen, sleep
from asyncio.subprocess import PIPE, STDOUT
from time import perf_counter
from discord import File
from io import StringIO
from importlib import import_module
from contextlib import redirect_stdout
from bot_api import _m_s


class Compiler(Cog):
    def __init__(self, bot: Bot):
        self.bot = bot

    @command(aliases=['expression', 'eval', 'calc'])
    async def evaluate(self, ctx: Context, *, content: str):
        try:
            await ctx.send(eval(content.removeprefix('```py').strip('`').replace('\u200A', ' ')))
        except Exception as e:
            await ctx.send(f'Error: ```\n{e}\n```')

    @command(aliases=['async_expression', 'aeval', 'async', 'await'])
    async def async_evaluate(self, ctx: Context, *, content: str):
        try:
            await ctx.send(await eval(content.removeprefix('```py').strip('`').replace('\u200A', ' ')))
        except Exception as e:
            await ctx.send(f'Error: ```\n{e}\n```')

    @command(aliases=['exec', 'compile', 'proc'])
    async def process(self, ctx: Context, *, content: str):
        _c = content.removeprefix('```py').strip('`').replace('\u200A', ' ')
        _p = await Popen('python', '-c', _c, stdout=PIPE, stderr=STDOUT)
        _t = perf_counter()
        _out = (await _p.communicate())[0]
        _t = perf_counter() - _t
        _resp1 = f'Ran\n```py\n{_c}``` in {_t} seconds with the status code of {_p.returncode} and the result of\n```\n{_out.decode()} ```'
        _resp2 = f'Ran in {_t} seconds with the status code of {_p.returncode} and the result of\n```\n{_out.decode()} ```'
        if len(_resp1) <= 2000:
            await ctx.reply(_resp1)
        elif len(_resp2) <= 2000:
            await ctx.reply(_resp2)
        else:
            await ctx.reply(_resp2.replace(f'\n```\n{_out.decode()} ```', '\n```\n'+_out.decode()[:2000-len(_resp2.replace(f'{_out.decode()} ```', '...```'))]+'...```'), file=File(StringIO(_out.decode()), 'out.txt'))

    @command(aliases=['sh', 'bash', 'shell'])
    async def spawn(self, ctx: Context, *, content: str):
        _c = content.removeprefix('```bash').removeprefix('```sh').strip('`').replace('\u200A', ' ')
        _p = await Sopen(_c, stdout=PIPE, stderr=STDOUT)
        _t = perf_counter()
        _out = (await _p.communicate())[0]
        _t = perf_counter() - _t
        _resp1 = f'Ran\n```bash\n{_c}``` in {_t} seconds with the status code of {_p.returncode} and the result of\n```\n{_out.decode()} ```'
        _resp2 = f'Ran in {_t} seconds with the status code of {_p.returncode} and the result of\n```\n{_out.decode()} ```'
        if len(_resp1) <= 2000:
            await ctx.reply(_resp1)
        elif len(_resp2) <= 2000:
            await ctx.reply(_resp2)
        else:
            await ctx.reply(_resp2.replace(f'\n```\n{_out.decode()} ```', '\n```\n'+_out.decode()[:2000-len(_resp2.replace(f'{_out.decode()} ```', '...```'))]+'...```'), file=File(StringIO(_out.decode()), 'out.txt'))

    @command(aliases=['literal_exec', 'exe', 'parse'])
    async def execute(self, ctx: Context, *, content: str):
        out = StringIO()
        with redirect_stdout(out):
            try:
                exec(content.removeprefix('```py').strip('`').replace('\u200A', ' '), dict(globals(), **locals()))
            except Exception as e:
                await ctx.reply(f'Error:\n```\n{e}\n```')
            else:
                if out.getvalue():
                    await ctx.reply(f'```py\n{out.getvalue()}```')

    @command(aliases=['async_exec', 'aexe', 'arun'])
    async def async_execute(self, ctx: Context, *, content: str):
        out = StringIO()
        with redirect_stdout(out):
            try:
                _scope = dict(globals(), **locals())
                exec(f'async def _async_exec():\n\t' + '\n\t'.join(content.removeprefix('```py').strip('`').replace('\u200A', ' ').split('\n')), _scope)
                await ctx.reply(await _scope['_async_exec']())
            except Exception as e:
                await ctx.reply(f'Error: ```\n{e}\n```')
            else:
                if out.getvalue():
                    await ctx.reply(f'```py\n{out.getvalue()}```')

    @command(aliases=['session', 'python', 'py'])
    async def ipython(self, ctx: Context):
        out = StringIO()
        while True:
            m = await ctx.bot.wait_for('message', check=lambda m: m.author.id == ctx.author.id and m.channel.id == ctx.channel.id)
            if m.content.lower().strip() == 'exit':
                break
            with redirect_stdout(out):
                try:
                    c = eval(compile(m.content, '<stdin>', 'eval'))
                except SyntaxError:
                    try:
                        c = exec(compile(m.content, '<stdin>', 'exec'))
                    except Exception as e:
                        c = f'{e.__class__.__name__}: {e}'
                except Exception as e:
                    c = f'{e.__class__.__name__}: {e}'
            await m.edit(content=f'```py\n>>> ' + '\n    '.join(m.content.split('\n')) + '```')
            if out.getvalue():
                await m.reply(f'```py\n{out.getvalue()}' + (f'\n{c}```' if c is not None else '```'))
            elif c is not None:
                await m.reply(f'```py\n{c}```')
            out.truncate(0)
        out.close()

    @command(aliases=['terminal', 'term', 'tmx'])
    async def fish(self, ctx: Context):
        while True:
            m = await ctx.bot.wait_for('message', check=lambda m: m.author.id == ctx.auth
            coded = m.coor.id and m.channel.id == ctx.channel.id)
            if m.content.lower().strip() == 'exit':
                break
            try:
                p = await Sopen(m.content, shell=True, stdout=PIPE, stderr=STDOUT)
                out = (await p.communicate())[0]
            except Exception as e:
                out = f'{e.__class__.__name__}: {e}'
            await m.edit(content=f'```bash\n$ > ' + '\n    '.join(m.content.split('\n')) + '```')
            if out:
                await m.reply(f'```bash\n{out}')

    @command(aliases=['iter', 'cycle', 'gen'])
    async def iterator(self, ctx: Context, delay: int = 1, *, content: str):
        try:
            iterator = eval(content.removeprefix('```py').strip('`').replace('\u200A', ' '))
            for e in iterator:
                await ctx.message.edit(content=e)
                await sleep(delay)
        except Exception as e:
            await ctx.send(f'Error:\n```\n{e}\n```')

    @command(aliases=['import', 'use', 'using'])
    async def imp(self, ctx: Context, *args: str):
        for m in args:
            if m:
                try:
                    if m in globals().keys():
                        raise ImportError(f'The module {m} was already imported')
                    globals()[m] = import_module(m)
                except Exception as e:
                    await ctx.reply(f'E: ```\n{e}\n```')

    @command(name='from')
    async def _from(self, ctx: Context, module: str, *targets: str):
        module = import_module(module)
        for t in targets:
            if t and t != 'import':
                try:
                    if t in globals():
                        raise ImportError(f'The module {module.__name__}.{t} was already imported')
                    globals()[t] = getattr(module, t)
                except Exception as e:
                    await ctx.reply(f'Error: ```\n{e}\n```')


def setup(bot: Bot):
    bot.add_cog(Compiler(bot))
    _m_s(__file__)
