import re
from ..command import *

@on('ready')
def init(bot):
	global emoji, emoji_re, emoji_sub
	emoji = bot.config['emoji']
	enclosure = emoji.get('_enclosure', ':') # The character that encloses the emoji - intentionally unescaped so config can use regexes
	emoji_re = re.compile('{0}\s*({1})\s*{0}'.format(enclosure, '|'.join(map(re.escape, emoji))), re.IGNORECASE)
	def emoji_sub(match):
		return emoji[match.group(1).strip().lower()]

@on('message')
async def insert_emoji(message):
	old = message.content
	new = emoji_re.sub(emoji_sub, old)
	if old != new:
		await message.edit(content=new)
