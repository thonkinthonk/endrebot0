from ..command import *

@command()
async def ping(ctx):
	return 'Pong!'

@command()
async def delete(ctx):
	await ctx.message.delete()

@command()
async def shutdown(ctx):
	await ctx.message.delete()
	await ctx.bot.close()
