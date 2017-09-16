import re
from ..command import *

sed_re = re.compile(r's/([^\/]+)/(.+)', re.IGNORECASE)

@on('message')
async def sed_sub(bot, message):
	m = sed_re.match(message.content)
	if not m: return
	async for msg in message.channel.history(before=message):
		if msg.author == message.author: break
	else:
		await message.edit(content='No substitutable message found.')
		await asyncio.sleep(2)
		await message.delete()
		return
	
	new_content = msg.content.replace(m.group(1), m.group(2))
	if message.content != new_content:
		await msg.edit(content=new_content)
	await message.delete()
