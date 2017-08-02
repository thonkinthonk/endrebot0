import asyncio, discord
from ..command import *

@command
async def ping(ctx):
	return 'Pong!'

@command
async def delete(ctx):
	await ctx.message.delete()

@command
async def game(ctx, game):
	await ctx.bot.change_presence(game=discord.Game(name=game))
	await ctx.message.delete()

afk_targets = None

async def afk_send(ctx, message_key, *args, **kwargs):
	global afk_targets
	if afk_targets is None:
		afk_targets = {channel.id: channel for channel in ctx.bot.get_all_channels() if isinstance(channel, discord.TextChannel)}
		afk_targets.update({mem.id: mem for mem in ctx.bot.get_all_members() if mem.bot})
	
	for info in ctx.bot.config['afk_messages']:
		if message_key in info:
			trigger = await afk_targets[info['dest']].send(info[message_key].format(*args, **kwargs))
			try:
				response = await ctx.bot.wait_for('message', check=lambda m: m.channel == trigger.channel, timeout=10)
				await response.ack()
			except asyncio.TimeoutError:
				pass
	
	await ctx.message.delete()

@command
async def afk(ctx, *args, **kwargs):
	await afk_send(ctx, 'afk_message', *args, **kwargs)

@command
async def unafk(ctx, *args, **kwargs):
	await afk_send(ctx, 'unafk_message', *args, **kwargs)
