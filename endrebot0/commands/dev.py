from discord.ext.commands import MemberConverter
from ..command import *

class repl:
	reaction = '\N{CLOCKWISE RIGHTWARDS AND LEFTWARDS OPEN CIRCLE ARROWS}'
	target_finder = MemberConverter()
	def __init__(self):
		self.__name__ = 'repl'
		self.start_message = None
		self.channel = None
		self.target = None
	
	async def start(self, ctx, target=None):
		self.start_message = ctx.message
		self.channel = ctx.channel
		self.target = target and await self.target_finder.convert(ctx, target)
		return 'REPL running for {}'.format(self.target or 'no target')
	
	async def stop(self, ctx):
		await self.start_message.delete()
		self.start_message = self.channel = self.target = None
		await ctx.message.delete()
	
	async def __call__(self, ctx):
		return (self.target, self.channel) if self.running else None
	
	async def on_message(self, bot, message):
		if message.channel == self.channel and message.id != self.start_message.id:
			await message.add_reaction(self.reaction)
	
	async def redo(self, bot, reaction, member):
		if member.id == bot.user.id and reaction.emoji == self.reaction and reaction.message.channel == self.channel:
			await reaction.message.delete()
			await self.channel.send(reaction.message.content)
	
	@property
	def running(self):
		return bool(self.channel)

repl = repl()
repl_cmd = command(repl)
repl_cmd.start = command(repl.start, '.repl.start') # Invalid identifier, but it stays in commands so it will auto-invoke
repl_cmd.stop = command(repl.stop, '.repl.stop')
on('message')(repl.on_message)
on('reaction_remove')(repl.redo)
