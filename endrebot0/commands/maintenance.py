import sys, importlib
from ..command import *

@command
async def shutdown(ctx):
	await ctx.message.delete()
	await ctx.bot.close()

@command
async def reload(ctx, *modules):
	for mod in modules:
		module = sys.modules['endrebot0.commands.%s' % mod]
		importlib.reload(module)
		ctx.bot.add_module(module)
	return 'Reloaded %d module(s)' % len(modules)
