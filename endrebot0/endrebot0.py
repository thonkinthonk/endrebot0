import discord, inspect
from . import log
from .command import *
from .fragment import *

class EndreBot(discord.Client):
	modules = {}
	commands = {}
	
	def __init__(self, config):
		super().__init__()
		self.config = config
		self.fragment = Fragmenter(*config['fragments'])
	
	def add_module(self, module):
		self.modules[module.__name__] = module
		if hasattr(module, 'commands'):
			self.commands.update(module.commands)
		if hasattr(module, 'listeners'):
			for event, listeners in module.listeners.items():
				if not hasattr(self, event):
					async def event_handler(self_, *args, **kwargs):
						await self_.call_listeners(*args, **kwargs)
					event_handler.__name__ = event
					setattr(type(self), event, event_handler)
					print(event_handler.__code__.co_name)
				self._listeners.setdefault(event, []).extend(listeners)
	
	async def on_ready(self):
		log.info('Logged in as %s (%s)' % (self.user, self.user.id))
		await self.call_listeners(self)
	
	async def on_message(self, message):
		if message.author != self.user: return
		
		ctx = Context(self, message)
		frag_results = []
		changed = False
		for frag in self.fragment(message.content):
			frag_ret = await frag.invoke(ctx)
			if frag_ret is not None:
				frag_results.append(frag_ret)
				changed |= frag_ret != frag.content
		if changed and frag_results:
			await message.edit(content=''.join(frag_results))
		
		await self.call_listeners(message)
	
	def run(self):
		super().run(self.config['token'], bot=False)
	
	async def call_listeners(self, *args, event_name=None, **kwargs):
		if event_name is None:
			try:
				frame = inspect.currentframe()
				event_name = frame.f_back.f_code.co_name
			finally:
				del frame
		if not event_name.startswith('on_'):
			event_name = 'on_' + event_name
		if event_name in self._listeners:
			for listener in self._listeners[event_name]:
				await listener(*args, **kwargs)
