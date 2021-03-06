from replit import db
from os import mkdir
from os.path import exists
default_settings = {'airdrop sniper': True, 'phrase sniper': True, 'nitro sniper': True, 'giveaway sniper': True, 'giveaway claimer': True, 'req sniper': False, 'invite sniper': False, 'claim token': '', 'phrase delay range': (4, 6), 'stats': {'sniped airdrops': 0, 'sniped phrases': 0}, 'giveaways': {}}
if not db and db is not None:
    db.update(default_settings)
df = dict(db)
for k, v in default_settings.items():
    if k not in df.keys():
        db[k] = v
if not exists('extensions'):
    mkdir('extensions')
if not exists('modules'):
    mkdir('modules')
if not exists('backups'):
    mkdir('backups')
if not exists('snippets'):
    mkdir('snippets')
