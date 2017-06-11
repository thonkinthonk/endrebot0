import sys

__all__ = ['command']

def command(name=None):
	def decorator(fn):
		command = Command(name or fn.__name__, fn)
		module = sys.modules[fn.__module__]
		if hasattr(module, 'commands'):
			commands = getattr(module, 'commands')
		else:
			commands = {}
			setattr(module, 'commands', commands)
		commands[name or fn.__name__] = command
		return command
	return decorator

class Command:
	def __init__(self, name, fn):
		self.name = name
		self.fn = fn
	
	async def invoke(self, bot, message):
		await self.fn(bot, message)
