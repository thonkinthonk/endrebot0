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
		new_content = []
		for frag in fragment(message.content):
			ctx.set_fragment(frag)
			frag_ret = await frag.invoke(ctx)
			if frag_ret:
				new_content.append(frag_ret)
		if new_content:
			await message.edit(content=''.join(new_content))
	
	def run(self, token):
		super().run(token, bot=False)
