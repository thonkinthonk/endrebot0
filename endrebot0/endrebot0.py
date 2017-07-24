import discord
from . import log
from .command import *
from .fragment import *

class EndreBot(discord.Client):
	modules = {}
	commands = {}
	
	def __init__(self):
		super().__init__()
		log.info('endrebot0 v0.4.0')
	
	def add_module(self, module):
		self.modules[module.__name__] = module
		self.commands.update(module.commands)
	
	async def on_ready(self):
		log.info('Logged in as %s (%s)' % (self.user, self.user.id))
	
	async def on_message(self, message):
		if message.author != self.user: return
		
		ctx = Context(self, message)
		frag_results = []
		changed = False
		for frag in fragment(message.content):
			frag_ret = await frag.invoke(ctx)
			if frag_ret is not None:
				frag_results.append(frag_ret)
				changed |= frag_ret != frag.content
		if changed and frag_results:
			await message.edit(content=''.join(frag_results))
	
	def run(self, token):
		super().run(token, bot=False)
