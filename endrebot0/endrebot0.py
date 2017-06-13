import discord
from . import log
from .fragment import fragment

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
		
		fragments = fragment(message.content)
		new_content = ''.join([(await frag.invoke(message)) for frag in fragments])
		if message.content != new_content:
			await message.edit(content=new_content)
	
	def run(self, token):
		super().run(token, bot=False)
