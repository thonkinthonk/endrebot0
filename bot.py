import discord
import asyncio
import messages
import os
from config import config

module_dir = 'commands'
for file in os.listdir(module_dir):
	if file == '__pycache__' or file == '__init__.py':
		continue
	__import__(module_dir + '.' + file[:-3]) #Remove '.py' from filename

print('endrebot0 v0.4.0')
client = discord.Client()

@client.event
@asyncio.coroutine
def on_ready():
	print('Logged in as %s (%s)' % (client.user.name, client.user.id))

@client.event
@asyncio.coroutine
def on_message(message):
	yield from messages.handle_message(client, message)

client.run(config['token'], bot=False)
