import messages
@messages.handler('echo')
def echo(client, message, content):
	print('Echo', content)
	yield from client.send_message(message.channel, content)
