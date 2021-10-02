from discord.ext.commands import Cog, Context, command, Bot
from discord import Embed
from os import listdir
from bot_api import _e_s, color


class Reload(Cog):
    def __init__(self, bot: Bot):
        self.bot = bot

    @command(aliases=['restart'])
    async def reload(self, ctx: Context, cog: str = None):
        if not cog:
            async with ctx.typing():
                embed = Embed(
                    title="Reloading all cogs!",
                    color=color(),
                    timestamp=ctx.message.created_at
                )
                for ext in listdir('extensions'):
                    if ext.endswith('.py') and not ext.startswith('_'):
                        try:
                            self.bot.unload_extension(f'extensions.{ext[:-3]}')
                            self.bot.load_extension(f'extensions.{ext[:-3]}')
                            embed.add_field(
                                name=f'Reloaded: `{ext}`',
                                value='\uFEFF',
                                inline=False
                            )
                        except Exception as e:
                            embed.add_field(
                                name=f'Failed to reload: `{ext}`',
                                value=e,
                                inline=False
                            )
                for ext in listdir('modules'):
                    if ext.endswith('.py') and not ext.startswith('_'):
                        try:
                            self.bot.unload_extension(f'modules.{ext[:-3]}')
                            self.bot.load_extension(f'modules.{ext[:-3]}')
                            embed.add_field(
                                name=f'Reloaded: `{ext}`',
                                value='\uFEFF',
                                inline=False
                            )
                        except Exception as e:
                            embed.add_field(
                                name=f'Failed to reload: `{ext}`',
                                value=e,
                                inline=False
                            )
                await ctx.reply(embed=embed)
        else:
            async with ctx.typing():
                embed = Embed(
                    title=f'Reloading cog {cog}',
                    color=color(),
                    timestamp=ctx.message.created_at
                )
                try:
                    self.bot.unload_extension(cog)
                    self.bot.load_extension(cog)
                    embed.add_field(
                        name=f"Reloaded: `{cog}`",
                        value='\uFEFF',
                        inline=False
                    )
                except Exception as e:
                    embed.add_field(
                        name=f"Failed to reload: `{cog}`",
                        value=e,
                        inline=False
                    )
            await ctx.reply(embed=embed)

def setup(bot: Bot):
    bot.add_cog(Reload(bot))
    _e_s(__file__)
