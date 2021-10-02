from discord.ext.commands import Cog, Bot, command, Context
from aiofiles import open as aopen
from bot_api import _m_s


class Files(Cog):
    def __init__(self, bot: Bot):
        self.bot = bot

    @command(aliases=['cat', 'concatenate', 'concat'])
    async def content(self, ctx: Context, file: str, rate: str = '0:1993'):
        try:
            rate = slice(*map(int, rate.split(':')))
            async with aopen(file, 'r') as f:
                await ctx.reply(f'```\n{(await f.read())[rate]}```')
        except Exception as e:
            await ctx.reply(f'❌ Error: ```\n{e}```')

    @command(aliases=['edit'])
    async def modify(self, ctx: Context, file: str, enc: str = None):
        async with aopen(file, 'r+') as f:
            msg = await ctx.reply(f'```{enc if enc else ""}\n{await f.read()}```')
            while True:
                try:
                    m = (await self.bot.wait_for('message_edit', check=lambda before, after: before.id == msg.id))[1]
                    if not m.content.startswith('```') or not m.content.endswith('```'):
                        await m.delete()
                        await (await ctx.channel.fetch_message(m.reference.message_id)).delete()
                        break
                    await f.seek(0)
                    await f.truncate(0)
                    await f.write(m.content.removeprefix(f'```{enc if enc else ""}\n').removesuffix('```').strip()+'\n')
                    await f.flush()
                except Exception as e:
                    await ctx.reply(f'❌ Error: ```{e}```')
                else:
                    await ctx.reply(f'✅ Saved changes to `{file}` successfully')

def setup(bot: Bot):
    bot.add_cog(Files(bot))
    _m_s(__file__)
