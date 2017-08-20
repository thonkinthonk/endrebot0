import math, string, unicodedata
from ..command import *
from discord.utils import get

abc_emoji = {letter: unicodedata.lookup('REGIONAL INDICATOR SYMBOL LETTER %s' % letter) for letter in string.ascii_uppercase}

@command
async def reactlevel(ctx, message_id, channel=None):
	if channel is None:
		channel = ctx.channel
	elif isinstance(channel, int):
		channel = get(ctx.bot.get_all_channels(), id=channel)
	elif isinstance(channel, str):
		channel = get(ctx.guild.text_channels, name=channel) or get(ctx.bot.get_all_channels(), name=channel)
	
	async for msg in channel.history(limit=100):
		if msg.id == message_id:
			break
	else:
		return 'Message not found'
	
	if not msg.reactions:
		return 'No reactions'
	
	target = math.ceil(sum([r.count for r in msg.reactions]) / len(msg.reactions))
	for react in msg.reactions:
		if react.count < target:
			await msg.add_reaction(react.emoji)
		elif react.count > target:
			await msg.remove_reaction(react.emoji, channel.guild.me)

@command
async def reactspell(ctx, react_message, message_id, channel=None):
	if len(react_message) != len(set(react_message)):
		return 'Message contains duplicate letters'
	
	if channel is None:
		channel = ctx.channel
	elif isinstance(channel, int):
		channel = get(ctx.bot.get_all_channels(), id=channel)
	elif isinstance(channel, str):
		channel = get(ctx.guild.text_channels, name=channel) or get(ctx.bot.get_all_channels(), name=channel)
	
	async for msg in channel.history(limit=100):
		if msg.id == message_id:
			break
	else:
		return 'Message not found'
	
	for letter in react_message.upper():
		await msg.add_reaction(abc_emoji[letter])
	
	await ctx.message.delete()
