from bot_api import prefix, run, clear
from discord import Status
from bot import Bot


# Clearing console
clear()

# Bot declaration & run
run(Bot(status=Status.offline, self_bot=True, case_insensitive=True, strip_after_prefix=True, command_prefix=prefix()))
