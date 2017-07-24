import asyncio, functools, inspect, sys

__all__ = ['command', 'Context']

def command(fn):
	"""Decorator for functions that should be exposed as commands."""
	module = sys.modules[fn.__module__]
	command_fn = fn if asyncio.iscoroutinefunction(fn) else asyncio.coroutine(fn)
	@functools.wraps(fn)
	async def wrapper(*args, **kwargs):
		try:
			frame = inspect.currentframe()
			ctx = frame.f_back.f_locals['ctx']
			return await command_fn(ctx, *args, **kwargs)
		finally:
			del frame
	vars(module).setdefault('commands', {})[fn.__name__] = wrapper
	return wrapper

def _message_prop(name):
	def getter(self):
		return self.__dict__.setdefault(name, getattr(self.message, name))
	
	def setter(self, val):
		self.__dict__[name] = val
	
	def deleter(self):
		del self.__dict__[name]
	
	return property(getter, setter, deleter)

def _channel_prop(name):
	def getter(self):
		return self.__dict__.setdefault(name, getattr(self.message.channel, name))
	
	def setter(self, val):
		self.__dict__[name] = val
	
	def deleter(self):
		del self.__dict__[name]
	
	return property(getter, setter, deleter)

def _guild_prop(name):
	def getter(self):
		return self.__dict__.setdefault(name, getattr(self.message.guild, name))
	
	def setter(self, val):
		self.__dict__[name] = val
	
	def deleter(self):
		del self.__dict__[name]
	
	return property(getter, setter, deleter)

class Context:
	def __init__(self, bot, message):
		self.bot = bot
		self.message = message
	
	channel = _message_prop('channel')
	guild = _message_prop('guild')
	author = _message_prop('author')
	send = _channel_prop('send')
	history = _channel_prop('history')
	pins = _channel_prop('pins')
	me = _guild_prop('me')
	
	def set_fragment(self, fragment):
		self.fragment = fragment
