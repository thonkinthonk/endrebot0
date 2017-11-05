import json, sys, importlib
from ..command import *

@command
async def shutdown(ctx):
	await ctx.message.delete()
	await ctx.bot.close()

@command
async def reload(ctx, *modules):
	for mod in modules:
		if mod == 'config':
			with open('config.json', encoding='utf-8') as f:
				ctx.bot.config = json.load(f)
		else:
			module_name = 'endrebot0.commands.{}'.format(mod)
			module = sys.modules.get(module_name)
			if module is not None:
				if hasattr(module, 'listeners'):
					del module.listeners
				if hasattr(module, 'commands'):
					del module.commands
			importlib.reload(module)
			ctx.bot.add_module(module)
			if hasattr(module, 'listeners'):
				for listener in module.listeners.get('on_ready', ()):
					await listener(ctx.bot)
	return 'Reloaded %d module(s)' % len(modules)
