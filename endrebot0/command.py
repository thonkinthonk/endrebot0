import sys

__all__ = ['command', 'Context']

def _message_prop(name):
	def getter(self):
		return self.__dict__.setdefault(name, getattr(self.message, name))
	
	def setter(self, val):
		self.__dict__[name] = val
	
	def deleter(self):
		del self.__dict__[name]
	
	return property(getter, setter, deleter)

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
	
	async def invoke(self, ctx):
		return await self.fn(ctx)

class Context:
	def __init__(self, bot, message):
		self.bot = bot
		self.message = message
	
	channel = _message_prop('channel')
	guild = _message_prop('guild')
	send = _message_prop('send')
	
	@send.getter
	def send(self):
		return self.__dict__.setdefault('send', self.message.channel.send)
	
	def set_fragment(self, fragment):
		self.fragment = fragment
		# TODO: parse args
