import json
from endrebot0 import EndreBot

bot = EndreBot()

with open('config/config.json') as f:
	cfg = json.load(f)
	bot.run(cfg['token'])
	log.shutdown()
