from colorama import Fore
from os import environ, listdir, system, name
from io import StringIO
from random import randint
from time import strftime


class Log:
    @staticmethod
    def module_load(module, m='Loading %s...'):
        print(f'{Fore.LIGHTWHITE_EX}( {strftime("%H:%M:%S")} ) [ {Fore.LIGHTGREEN_EX}MODULE{Fore.LIGHTWHITE_EX} ] {Fore.LIGHTYELLOW_EX}{m%module}{Fore.RESET}')

    @staticmethod
    def module_load_err(module, err, m='Failed loading %s: %s'):
        print(f'{Fore.LIGHTWHITE_EX}( {strftime("%H:%M:%S")} ) [ {Fore.LIGHTRED_EX}MODULE{Fore.LIGHTWHITE_EX} ] {Fore.LIGHTRED_EX}{m%(module, Fore.RED+str(err)+Fore.LIGHTRED_EX)}{Fore.RESET}')

    @staticmethod
    def module_load_success(module, m='Loaded %s sucessfully!'):
        print(f'{Fore.LIGHTWHITE_EX}( {strftime("%H:%M:%S")} ) [ {Fore.LIGHTGREEN_EX}MODULE{Fore.LIGHTWHITE_EX} ] {Fore.LIGHTYELLOW_EX}{m%module}{Fore.RESET}')

    @staticmethod
    def extension_load(extension, m='Loading %s...'):
        print(f'{Fore.LIGHTWHITE_EX}( {strftime("%H:%M:%S")} ) [ {Fore.LIGHTGREEN_EX}EXTENSION{Fore.LIGHTWHITE_EX} ] {Fore.LIGHTYELLOW_EX}{m%extension}{Fore.RESET}')

    @staticmethod
    def extension_load_err(extension, err, m='Failed loading %s: %s'):
        print(f'{Fore.LIGHTWHITE_EX}( {strftime("%H:%M:%S")} ) [ {Fore.LIGHTRED_EX}EXTENSION{Fore.LIGHTWHITE_EX} ] {Fore.LIGHTRED_EX}{m%(extension, Fore.RED+str(err)+Fore.LIGHTRED_EX)}{Fore.RESET}')

    @staticmethod
    def extension_load_success(extension, m='Loaded %s sucessfully!'):
        print(f'{Fore.LIGHTWHITE_EX}( {strftime("%H:%M:%S")} ) [ {Fore.LIGHTGREEN_EX}EXTENSION{Fore.LIGHTWHITE_EX} ] {Fore.LIGHTYELLOW_EX}{m%extension}{Fore.RESET}')

    @staticmethod
    def log(message='', section='BOT'):
        print(f'{Fore.LIGHTWHITE_EX}( {strftime("%H:%M:%S")} ) [ {Fore.LIGHTCYAN_EX}{section}{Fore.LIGHTWHITE_EX} ] {Fore.LIGHTYELLOW_EX}{message}{Fore.RESET}')

    @staticmethod
    def success(message='', section='BOT'):
        print(f'{Fore.LIGHTWHITE_EX}( {strftime("%H:%M:%S")} ) [ {Fore.GREEN}{section}{Fore.LIGHTWHITE_EX} ] {Fore.LIGHTGREEN_EX}{message}{Fore.RESET}')

    @staticmethod
    def warn(message='', section='BOT'):
        print(f'{Fore.LIGHTWHITE_EX}( {strftime("%H:%M:%S")} ) [ {Fore.LIGHTRED_EX}{section}{Fore.LIGHTWHITE_EX} ] {Fore.LIGHTRED_EX}{message}{Fore.RESET}')

    @staticmethod
    def err(message='', section='BOT'):
        print(f'{Fore.LIGHTWHITE_EX}( {strftime("%H:%M:%S")} ) [ {Fore.RED}{section}{Fore.LIGHTWHITE_EX} ] {Fore.RED}{message}{Fore.RESET}')


def _m_s(m):
    Log.module_load_success(m.split('/')[-1].removeprefix('_').removesuffix('.py').capitalize())


def _e_s(e):
    Log.extension_load_success(e.split('/')[-1].removeprefix('_').removesuffix('.py').capitalize())


def partial(func, *args, **kwargs):
    return lambda: func(*args, **kwargs)


def ka():
    from flask import Flask
    from threading import Thread
    from logging import getLogger
    getLogger('werkzeug').disabled = True
    environ['WERKZEUG_RUN_MAIN'] = 'true'
    (a := Flask('')).route('/')(lambda: '')
    Thread(target=partial(a.run, host='0.0.0.0', port=8080, threaded=True), daemon=True).start()


def color():
    return randint(0x000000, 0xffffff)


def clear():
    system('cls') if name == 'nt' else system('clear')


def load_modules(bot):
    for m in listdir('modules'):
        if m.endswith('.py'):
            Log.module_load(m.removeprefix('_').removesuffix('.py').capitalize())
            try:
                bot.load_extension(f'modules.{m.removesuffix(".py")}')
            except Exception as e:
                Log.module_load_err(m, e)


def load_extensions(bot):
    for ext in listdir('extensions'):
        if ext.endswith('.py'):
            Log.extension_load(ext.removeprefix('_').removesuffix('.py').capitalize())
            try:
                bot.load_extension(f'extensions.{ext.removesuffix(".py")}')
            except Exception as e:
                Log.extension_load_err(ext, e)


def prefix():
    from discord.ext.commands import when_mentioned, when_mentioned_or
    def _(bot, message):
        if message.author == bot.user:
            return when_mentioned_or('.')(bot, message)
        elif message.author.id == 804385505814118453:
            return when_mentioned(bot, message)
        else:
            return []
    return _


class FormatDict(dict):
    def __missing__(self, key):
        return f'{{key}}'


async def dump_airdrop(client, message):
    val = message.embeds[0].description.split('airdrop of')[1].split(')')[0].strip()
    await client.http._HTTPClient__session.post(
        environ['WEBHOOK'],
        json={
        'content': '',
        'embeds': [
            {
                'title': 'Airdrop sniped',
                'description': f'Sniped an airdrop with a value of {val}) in <#{message.channel.id}> (channel from {message.channel.guild.name}).\n[[ Jump to message ]]({message.jump_url})',
                'author': {
                    'name': f'{client.user}',
                    'icon_url': str(client.user.avatar_url)
                    },
                'color': 0x1abc9c
            }
            ],
        'username': f"{client.user}'s selfbot",
        'avatar_url': str(client.user.avatar_url)
        })


async def dump_phrasedrop(client, message):
    val = message.embeds[0].description.split('split the')[1].split(')')[0].strip()
    await client.http._HTTPClient__session.post(
        environ['WEBHOOK'],
        json={
            'content': '',
            'embeds': [{
                'title': 'Phrasedrop sniped',
                'description': f'Sniped a phrasedrop with a value of {val}) in <#{message.channel.id}> (channel from {message.channel.guild.name}).\n[[ Jump to message ]]({message.jump_url})',
                'author': {
                    'name': f'{client.user}',
                    'icon_url': str(client.user.avatar_url)
                    },
                'color': 0x1abc9c
                }],
            'username': f"{client.user}'s selfbot",
            'avatar_url': str(client.user.avatar_url)
            })


async def dump_giveaway(client, message):
    await client.http._HTTPClient__session.post(
        environ['WEBHOOK'],
        json={
            'content': '',
            'embeds': [{
                'title': 'Giveaway sniped',
                'description': f'Sniped a giveaway with a prize of {message.embeds[0].author.name} in <#{message.channel.id}> (channel from {message.channel.guild.name}). Ends on {message.embeds[0].description.split("Ends: ")[1]}\n[[ Jump to message ]]({message.jump_url})',
                'author': {
                    'name': f'{client.user}',
                    'icon_url': str(client.user.avatar_url)
                    },
                'color': 0xf75482
                }],
            'username': f"{client.user}'s selfbot",
            'avatar_url': str(client.user.avatar_url)
            })


async def dump_win(client, message, mg):
    lst = '\n\t-\t'+'\n\t-\t'.join(map(str, mg))
    await client.http._HTTPClient__session.post(
        environ['WEBHOOK'],
        json={
            'content': '',
            'embeds': [{
                'title': 'Giveaway won!',
                'description': f'Won a giveaway in <#{message.channel.id}> (channel from {message.channel.guild.name}).\nMessaged: {lst}\n\n[[ Jump to message ]]({message.jump_url})',
                'author': {
                    'name': f'{client.user}',
                    'icon_url': str(client.user.avatar_url)
                    },
                'color': 0x71e62e
                }],
            'username': f"{client.user}'s selfbot",
            'avatar_url': str(client.user.avatar_url)
            })


async def dump_nitro(client, message, response):
    await client.http._HTTPClient__session.post(
        environ['WEBHOOK'],
        json={
            'content': '',
            'embeds': [{
                'title': 'Sniped Nitro!',
                'description': f'Sniped Nitro in <#{message.channel.id}>.\nThe status code was **{response.status_code}**\n\n[[ Jump to message ]]({message.jump_url})',
                'author': {
                    'name': f'{client.user}',
                    'icon_url': str(client.user.avatar_url)
                    },
                'color': 0x71e62e
                }],
            'username': f"{client.user}'s selfbot",
            'avatar_url': str(client.user.avatar_url)
            })
