from ..command import *

@command()
async def ping(bot, msg):
	await msg.edit(content='Pong!')

@command()
async def shutdown(bot, msg):
	await bot.close()
