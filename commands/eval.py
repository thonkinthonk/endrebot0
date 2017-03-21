import discord
import messages

@messages.handler('eval')
def evaluate(client, message, content):
	code = content
	if content.startswith('```'):
		code = content[content.find('\n')+1:content.rfind('\n')]
	embed = discord.Embed()
	embed.type='rich'
	embed.add_field(name='Code', value='```Python\n%s\n```' % code, inline=False)
	try:
		ret = eval(code)
		embed.title = 'Python Evaluation - Success'
		embed.color = 0x00FF00
		embed.add_field(name='Output', value='```\n%s\n```' % str(ret), inline=False)
	except Exception as err:
		embed.title = 'Python Evaluation - Error'
		embed.color = 0xFF0000
		embed.add_field(name='Error', value='```\n%s\n```' % str(err))
	yield from client.send_message(message.channel, embed=embed)

@messages.handler('exec')
def execute(client, message, content):
	code = content
	if content.startswith('```'):
		code = content[content.find('\n')+1:content.rfind('\n')]
	embed = discord.Embed()
	embed.type='rich'
	embed.add_field(name='Code', value='```Python\n%s\n```' % code, inline=False)
	try:
		exec(code)
		embed.title = 'Python Execution - Success'
		embed.color = 0x00FF00
	except Exception as err:
		embed.title = 'Python Execution - Error'
		embed.color = 0xFF0000
		embed.add_field(name='Error', value='```\n%s\n```' % str(err))
	yield from client.send_message(message.channel, embed=embed)
