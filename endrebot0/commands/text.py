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

@command
def box(ctx, text):
	text = text.upper().replace(' ', '')
	top = ' '.join(text)
	center_spacing = ' ' * (2 * len(text) - 3)
	sides = (left + center_spacing + right for left, right in zip(text[1:-1], reversed(text[1:-1])))
	return '\n'.join(('```', top, *sides, ''.join(reversed(top)), '```'))

@command
def arrow(ctx, text, dir=0):
	left, up = not (dir % 2), not (dir >> 1)
	reverse_diag = left ^ up
	text = text.upper().replace(' ', '')
	rows = [[' ' for _ in text] for _ in text] # Grid of spaces to fill in
	rows[0 if up else -1][:] = list(text)
	for i, (row, letter) in enumerate(zip(rows, reversed(text) if reverse_diag else text)):
		row[-i-1 if reverse_diag else i] = letter
		rows[i][0 if left else -1] = letter
	return '\n'.join(('```', *map(' '.join, rows), '```'))

@command
def xbox(ctx, text):
	text = text.upper().replace(' ', '')
	rows = [[' ' for _ in text + '  '] for _ in text + '  '] # Add two extra rows and columns
	rows[0][1:-1] = text
	for i, (row, letter, rev_letter) in enumerate(zip(rows[1:-1], text, reversed(text))):
		row[0], row[-1], row[i+1] = (letter,) * 3
		row[-i-2] = rev_letter
	rows[-1][1:-1] = text
	return '\n'.join(('```', *map(' '.join, rows), '```'))
