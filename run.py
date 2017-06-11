import json, importlib, pkgutil
from endrebot0 import EndreBot, log

bot = EndreBot()

for _, name, _ in pkgutil.iter_modules(['endrebot0/commands']):
	log.debug('Loading module %s', name)
	module = importlib.import_module('endrebot0.commands.' + name)
	bot.add_module(module)

with open('config/config.json') as f:
	cfg = json.load(f)
	bot.run(cfg['token'])
	log.shutdown()
