import re, requests
from ..command import *

@on('ready')
def init(bot):
	global emoji, emoji_re, emoji_sub
	emoji = bot.config['emoji']
	enclosure = emoji.get('_enclosure', ':') # The character that encloses the emoji - intentionally unescaped so config can use regexes
	emoji_re = re.compile('{0}\s*({1})\s*{0}'.format(enclosure, '|'.join(map(re.escape, emoji))))
	def emoji_sub(match):
		return emoji[match.group(1).strip()]

@on('message')
async def insert_emoji(bot, message):
	old = message.content
	new = emoji_re.sub(emoji_sub, old)
	if old != new:
		await message.edit(content=new)

@command
async def copy_emoji(ctx, emoji, name=None):
	with requests.get(emoji.url) as image_data:
		new_emoji = await ctx.guild.create_custom_emoji(name=name or emoji.name, image=image_data.content)
	return new_emoji
