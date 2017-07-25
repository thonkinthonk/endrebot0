from ..command import *

@command
async def shutdown(ctx):
	await ctx.message.delete()
	await ctx.bot.close()
