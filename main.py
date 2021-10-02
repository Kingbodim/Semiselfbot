import bot_api as api
modules = api.modules

# Keep alive (ignore this, just for Uptime Robot to ping the whole bot)
a = modules.flask.Flask(''); a.route('/')(lambda: ''); modules.threading.Thread(target=api.partial_nout(a.run, host='0.0.0.0', port=8080, threaded=True), daemon=True).start()

# Clearing console
modules.os.system('clear')

# Bot declaration
bot = modules.discord.ext.commands.Bot(status=modules.Status.offline, self_bot=True, case_insensitive=True, command_prefix=api.prefix)
api.setup(bot)
bot.api = api

# Globalised variables for the bot
bot.ext.sniped_airdrops = 0
bot.ext.sniped_phrases = 0

# Just for retrieving uptime
with open('uptime register.txt', 'a') as f:
    f.write(str(bot.started) + '\n')

# Run bot
bot.run(modules.os.environ['TOKEN'])
