import json, sys, importlib
from ..command import *

@command
async def shutdown(ctx):
	await ctx.message.delete()
	await ctx.bot.close()

@command
def reload(ctx, *modules):
	for mod in modules:
		if mod == 'config':
			with open('config.json', encoding='utf-8') as f:
				ctx.bot.config = json.load(f)
		else:
			module = sys.modules['endrebot0.commands.%s' % mod]
			if hasattr(module, 'listeners'):
				del module.listeners
			if hasattr(module, 'commands'):
				del module.commands
			importlib.reload(module)
			ctx.bot.add_module(module)
	return 'Reloaded %d module(s)' % len(modules)
