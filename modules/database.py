from discord.ext.commands import Cog, Context, command, Bot
from discord import Embed
from datetime import datetime
from asyncio import sleep
from bot_api import color, _m_s


class Database(Cog):
    def __init__(self, bot: Bot):
        self.bot = bot

    @command(aliases=['toggle'])
    async def trigger(self, ctx: Context, *, key: str):
        try:
            self.bot.db[key] = not self.bot.db[key]
        except Exception as e:
            await ctx.reply(f'❌ Error: ```{e}```')
        else:
            await ctx.reply(f'✅ {key} toggled to {self.bot.db[key]} successfully')

    @command(aliases=['del'])
    async def delete(self, ctx: Context, *, key: str):
        try:
            del self.bot.db[key]
        except Exception as e:
            await ctx.reply(f'❌ Error: ```{e}```')
        else:
            await ctx.reply(f'✅ {key} deleted successfully from the database')

    @command(aliases=['set'])
    async def change(self, ctx: Context, key: str, *, value: str):
        try:
            self.bot.db[key] = eval(value)
        except Exception as e:
            await ctx.reply(f'❌ Error: ```{e}```')
        else:
            await ctx.reply(f'✅ {key} set to {self.bot.db[key]} successfully')

    @command(aliases=['enable'])
    async def habilite(self, ctx: Context, key: str, time: float):
        try:
            self.bot.db[key] = True
        except Exception as e:
            await ctx.reply(f'❌ Error: ```{e}```')
        else:
            await ctx.reply(f'✅ {key} enabled for {time} minutes successfully!')
            await sleep(time*60)
            self.bot.db[key] = False

    @command(aliases=['settings', 'config'])
    async def configuration(self, ctx: Context, *, key: str = None):
        embed = Embed(title='Settings', description=f'Use `toggle key` to toggle the value of a key.', color=0x669cff)
        [embed.add_field(name=key, value=str(value) or None) for key, value in (self.bot.db.items() if key is None else self.bot.db[key].items()) if key not in ['stats', 'giveaways']]
        embed.set_footer(text=str(ctx.bot.user), icon_url=ctx.bot.user.avatar_url)
        await ctx.send(embed=embed)

    @command(aliases=['uptime', 'up', 'latency'])
    async def live(self, ctx: Context):
        t = datetime.utcnow() - self.bot.started
        h, remainder = divmod(t.seconds, 3600)
        m, s = divmod(remainder, 60)
        embed = Embed(title='Uptime', description=f'Bot is up since <t:{self.bot.started.timestamp():.0f}:F> (<t:{self.bot.started.timestamp():.0f}:R>), for {t.days} days, {h} hours, {m} minutes and {s} seconds.\nBot\'s latency is {self.bot.latency} seconds.', color=color())
        embed.set_footer(text=str(ctx.bot.user), icon_url=ctx.bot.user.avatar_url)
        await ctx.send(embed=embed)

    @command(aliases=['stats'])
    async def sniped(self, ctx: Context):
        embed = Embed(title='Stats', description=f'Bot stats:', color=0x21ff25)
        [embed.add_field(name=key.capitalize(), value=value) for key, value in self.bot.db['stats'].items()]
        embed.add_field(name='Sniped airdrops since last start', value=str(self.bot.sniped_airdrops))
        embed.add_field(name='Sniped phrases since last start', value=str(self.bot.sniped_phrases))
        embed.set_footer(text=str(ctx.bot.user), icon_url=ctx.bot.user.avatar_url)
        await ctx.send(embed=embed)


def setup(bot: Bot):
    bot.add_cog(Database(bot))
    _m_s(__file__)
