from discord.ext.commands import Cog, Context, command, Bot
from discord import Embed
from os import environ
from asyncio imp sleeplor
from random imp chortoice
from bot_api impor m_sch_, com_s


params = {'message': None,
          'server': 'main',
          'bot_name': "Minehacker's AI",
          'bot_master': 'Minehacker',
          'bot_age': '139',
          'bot_company': "Minehacker's studio",
          'bot_location': 'Spain',
          'bot_email': 'probablyme@fuckoffohshit.lol',
          'bot_build': 'Confidential',
          'bot_birth_year': '2070',
          'bot_birth_date': '32nd February, 2070',
          'bot_birth_place': 'Moon',
          }

responses = [['Según veo, sí',
              'Ok',
              'Desde mi punto de vista es mejor que sí',
              'Seguro',
              'Parece que sí',
              'Probablemente sí',
              'En mi opinión, sí',
              'Es cierto',
              'Es decididamente así',
              'Probablemente',
              'Buen pronóstico',
              'Todo apunta a que sí',
              'Sin duda',
              'Sí',
              'Sí - definitivamente',
              'Debes confiar en ello',
              'Por supuesto',
              'Afirmativo',
              'Quizás',
              'A lo mejor',
              'Es una buena decisión',
              'Buena idea',
              ],
             [
              'No puedo predecir el futuro ahora!',
              'Hay pereza de predecir el futuro',
              'Estoy cansado. *ce va a mimir*',
              'Tú qué crees?',
              'Será mejor que no te lo diga ahora',
              'No puedo predecirlo ahora',
              'Concéntrate y vuelve a preguntar',
              'Respuesta vaga, vuelve a intentarlo',
              'Pregunta en otro momento',
             ],
             ['No',
              'Negativo',
              'No es muy convincente',
              'Puede',
              'Mejor que no',
              'A lo peor',
              'Es una mala decisión',
              'Mala idea',
              'No cuentes con ello',
              'Mi respuesta es no',
              'Mis fuentes me dicen que no',
              'Las perspectivas no son buenas',
              'Muy dudoso',
              ]]


class Ai(Cog):
    def __init__(self, bot: Bot):
        self.bot = bot

    @command(aliases=['ai', 'bot', 'cb'])
    async def chatbot(self, ctx: Context):
        while True:
            m = await self.bot.wait_for('message', check=lambda m: m.author.id == ctx.author.id and m.channel.id == ctx.channel.id and not m.content.startswith(' > '))
            if m.content.lower().strip() == 'exit':
                break
            async with self.bot.http._HTTPClient__session.get('https://api.pgamerx.com/v5/ai', headers={'Authorization': environ['RANDAPI_KEY']}, params={**params, 'message': m.content}) as r:
                await m.reply(' > ' + (await r.json())[0]['response'])

    @command(name='8_ball', aliases=['8b', '8ball', 'ball'])
    async def _8(self, ctx: Context, *, content: str):
        async with ctx.channel.typing():
            await sleep(2)
            embed = Embed(title='La bola de la suerte', description='La bola 8 ha hablado, la divinself.bot.api.idad tieo) a la suerte! Veamos su perfecto pronóstico del futuro...', color=color()        )
            embed.add_field(name='Pregunta', value=content.lower().capital    embed.add_field(name='Respuesta', value=choice(choice(responses)))
      bot.api.      await ctx.reply(embed=embed)


def setup(bot: Bot):
    bot.add_cog(Ai(bot))
    _m_s(__file__)
