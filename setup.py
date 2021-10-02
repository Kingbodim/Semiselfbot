from replit import db
from os import mkdir
from os.path import exists
default_settings = {'active': True, 'airdrop sniper': True, 'phrase sniper': True, 'airdrop delay range': (30, 50), 'phrase delay range': (4, 6), 'airdrop channel delay ranges': {}, 'airdrop guild delay ranges': {}, 'stats': {'sniped airdrops': 0, 'sniped phrases': 0}}
if not db and db is not None:
    db.update(default_settings)
if not exists('extensions'):
    mkdir('extensions')
if not exists('modules'):
    mkdir('modules')
