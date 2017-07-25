import discord
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
