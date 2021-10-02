class Modules(dict):
    from importlib import import_module as __i
    def __missing__(self, key):
        self[key] = self.__class__.__i(key)

    def __getattr__(self, attr):
        return self[attr]
    
    def __setattr__(self, attr, value):
        self[attr] = value


modules = Modules()
Fore = modules.colorama.Fore
environ, listdir = modules.os.environ, modules.os.listdir
redirect_stdout, redirect_stderr = modules.contextlib.redirect_stdout, modules.contextlib.redirect_stderr
StringIO = modules.io.StringIO
when_mentioned_or, when_mentioned = modules.discord.ext.commands.when_mentioned_or, modules.discord.ext.commands.when_mentioned
randint = modules.random.randint
strftime = modules.time.strftime


class Log:
    @classmethod
    def module_load(cls, module, m='Loading %s...'):
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
        print(f'{Fore.LIGHTWHITE_EX}( {strftime("%H:%M:%S")} ) [ {Fore.LIGHTRED_EX}{section}{Fore.LIGHTWHITE_EX} ] {Fore.LIGHTYELLOW_EX}{message}{Fore.RESET}')

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


def color():
    return randint(0x000000, 0xffffff)


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


def setup(bot):
    bot.ext = object()
    bot.ext.modules = modules
    bot.db = modules.replit.db
    bot.started = modules.datetime.datetime.utcnow()
    load_modules(bot)
    load_extensions(bot)


def prefix(bot, message):
    if message.author == bot.user:
        return when_mentioned_or('.')(bot, message)
    elif message.author.id == 890636026446479430:
        return when_mentioned(bot, message)
    else:
        return []


def partial(func, *args, **kwargs):
    return lambda: func(*args, **kwargs)


def partial_nout(func, *args, **kwargs):
    def _():
        with redirect_stdout(StringIO()) and redirect_stderr(StringIO()):
            func(*args, **kwargs)

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
