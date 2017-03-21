import discord
import messages

@messages.handler('servers')
def servers(client, message, content):
	yield from display_servers(client, message.channel, client.user.name + "'s Servers", client.servers)

@messages.handler('shared')
def shared(client, message, content):
	uid = content.strip()
	if content.startswith('<@') and content.endswith('>'):
		uid = content[2:-1]
	servers = []
	name = None
	for member in client.get_all_members():
		if member.id == uid:
			servers.append(member.server)
			if not name: name = member.name
	yield from display_servers(client, message.channel, "%s's and %s's Servers" % (client.user.name, name), servers)

def display_servers(client, channel, title, servers):
	embed = discord.Embed()
	embed.type = 'rich'
	embed.title = title
	embed.color = 0x00C8FB
	for server in servers:
		embed.add_field(name=server.name, value=str(server.id), inline=True)
	yield from client.send_message(channel, embed=embed)
