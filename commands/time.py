import messages
import asyncio

clock_emoji = [chr(0x1F55B)] # 12:00 is at the end, but should be at the beginning
for i in range(11):
	clock_emoji.append(chr(0x1F550 + i)) # i o'clock

@messages.handler('clock')
def clock(client, message, content):
	for clock in clock_emoji:
		yield from client.edit_message(message, clock)
		yield from asyncio.sleep(1)
	return False
