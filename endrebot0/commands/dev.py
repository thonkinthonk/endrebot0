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
		self.cleanup = False
	
	async def start(self, ctx, target=None):
		self.start_message = ctx.message
		self.channel = ctx.channel
		self.target = target and await self.target_finder.convert(ctx, target)
		self.cleanup = bool(self.target and self.channel.permissions_for(ctx.me).manage_messages)
		return 'REPL running for {} ({})'.format(self.target or 'no target', self.cleanup)
	
	async def stop(self, ctx):
		channel, self.channel = self.channel, None # Stop the repl session without losing reference to the channel
		async for msg in channel.history(after=self.start_message):
			if msg.author == ctx.me and msg.reactions:
				await msg.remove_reaction(self.reaction, ctx.me) # Fails silently; reactions check is just for efficiency
		await self.start_message.delete()
		self.start_message = self.target = None
		await ctx.message.delete()
	
	async def __call__(self, ctx):
		return (self.target, self.channel) if self.running else None
	
	async def on_message(self, bot, message):
		if message.channel == self.channel and message.id != self.start_message.id:
			await message.add_reaction(self.reaction)
	
	async def redo(self, bot, reaction, member):
		if member.id != bot.user.id or reaction.emoji != self.reaction or reaction.message.channel != self.channel:
			return
		
		message = reaction.message
		if self.cleanup:
			async for msg in message.channel.history(after=message):
				if msg.author == self.target:
					await msg.delete()
		
		await message.delete()
		await self.channel.send(message.content)
	
	@property
	def running(self):
		return bool(self.channel)

repl = repl()
repl_cmd = command(repl)
repl_cmd.start = command(repl.start, '.repl.start') # Invalid identifier, but it stays in commands so it will auto-invoke
repl_cmd.stop = command(repl.stop, '.repl.stop')
on('message')(repl.on_message)
on('reaction_remove')(repl.redo)
