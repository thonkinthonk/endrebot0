import discord
from . import log

class EndreBot(discord.Client):
	def __init__(self):
		super().__init__()
		log.info('endrebot0 v0.4.0')
	
	async def on_ready(self):
		log.info('Logged in as %s (%s)' % (self.user, self.user.id))
	
	async def on_message(self, message):
		if message.author != self.user: return
		if message.content == 'ping':
			await message.edit(content='Pong!')
		elif message.content == 'shutdown':
			await self.close()
	
	def run(self, token):
		super().run(token, bot=False)
