from discord.ext.commands import Cog, Context, command, Bot
from discord import Embed
from os.path import exists
from aiofiles import open as aopen
from bot_api import color, _m_s


class Extensions(Cog):
    def __init__(self, bot: Bot):
        self.bot = bot

    @command(aliases=['ext'])
    async def extension(self, ctx: Context, extension: str):
        if not exists(f'extensions/{extension}.py'):
            async with aopen(f'extensions/{extension}.py', 'w') as f, aopen('extensions/template.txt', 'r') as r:
                await f.write((await r.read()).format(name=extension.capitalize()))
        async with aopen(f'extensions/{extension}.py', 'r+') as f:
            msg = await ctx.reply(f'```py\n{await f.read()}```')
            while True:
                try:
                    m = (await self.bot.wait_for('message_edit', check=lambda before, after: before.id == msg.id))[1]
                    if not m.content.startswith('```py') or not m.content.endswith('```'):
                        await m.delete()
                        await (await ctx.channel.fetch_message(m.reference.message_id)).delete()
                        break
                    await f.seek(0)
                    await f.truncate(0)
                    await f.write(m.content.removeprefix('```py\n').removesuffix('```').strip()+'\n')
                    await f.flush()
                    if f'extensions.{extension}' in self.bot.extensions:
                        self.bot.reload_extension(f'extensions.{extension}')
                    else:
                        self.bot.load_extension(f'extensions.{extension}')
                except Exception as e:
                    await ctx.reply(f'❌ Error: ```{e}```')
                else:
                    await ctx.reply(f'✅ Saved changes to `{extension.capitalize()}` successfully')

    @command(aliases=['mod'])
    async def module(self, ctx: Context, module: str):
        if not exists(f'modules/{module}.py'):
            async with aopen(f'modules/{module}.py', 'w') as f, aopen('modules/template.txt', 'r') as r:
                await f.write((await r.read()).format(name=module.capitalize()))
        async with aopen(f'modules/{module}.py', 'r+') as f:
            msg = await ctx.reply(f'```py\n{await f.read()}```')
            while True:
                try:
                    m = (await self.bot.wait_for('message_edit', check=lambda before, after: before.id == msg.id))[1]
                    if not m.content.startswith('```py') or not m.content.endswith('```'):
                        await m.delete()
                        await (await ctx.channel.fetch_message(m.reference.message_id)).delete()
                        break
                    await f.seek(0)
                    await f.truncate(0)
                    await f.write(m.content.removeprefix('```py\n').removesuffix('```').strip()+'\n')
                    await f.flush()
                    if f'modules.{module}' in self.bot.extensions:
                        self.bot.reload_extension(f'modules.{module}')
                    else:
                        self.bot.load_extension(f'modules.{module}')
                except Exception as e:
                    await ctx.reply(f'❌ Error: ```{e}```')
                else:
                    await ctx.reply(f'✅ Saved changes to `{module.capitalize()}` successfully')

    @command(aliases=['load', 'le'])
    async def load_extension(self, ctx: Context, extension: str):
        try:
            self.bot.load_extension(extension)
        except Exception as e:
            await ctx.reply(f'❌ Error: ```\n{e}```')
        else:
            await ctx.reply(f'✅ {extension.capitalize()} extension has been loaded successfully!')

    @command(aliases=['unload', 'ue'])
    async def unload_extension(self, ctx: Context, extension: str):
        try:
            self.bot.unload_extension(extension)
        except Exception as e:
            await ctx.reply(f'❌ Error: ```\n{e}```')
        else:
            await ctx.reply(f'✅ {extension.capitalize()} extension has been unloaded successfully!')

    @command(aliases=['extensions', 'module_list', 'modules'])
    async def extension_list(self, ctx: Context):
        await ctx.reply(embed=Embed(title='Extensions & modules', description=f'Use `{ctx.prefix}extension <extension>` or `{ctx.prefix}module <module>` to edit and create extensions and modules.\n\n```\n'+'\n'.join(self.bot.extensions.keys())+'```', color=color()))


def setup(bot: Bot):
    bot.add_cog(Extensions(bot))
    _m_s(__file__)
