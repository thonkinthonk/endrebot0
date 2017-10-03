import functools, itertools
from collections.abc import Iterator
from discord.utils import get
from ..command import *

@command
def getone(ctx, itr, *checks, **attrs):
	return next(ExtendedFilter(itr, *checks, **attrs), None)

@command
def getall(ctx, itr, *checks, **attrs):
	return list(ExtendedFilter(itr, *checks, **attrs))

@command
def member(ctx, keyless=None, all=True, **attrs):
	members = list(ctx.guild.members)
	if all: members.extend(ctx.bot.get_all_members())
	if isinstance(keyless, int):
		attrs['id'] = keyless
		checks = ()
	elif isinstance(keyless, str):
		checks = (lambda mem: keyless in (mem.name, str(mem), mem.display_name),)
	elif keyless is not None:
		return 'Unable to infer key from {0.module.__name__}.{0.__qualname__}'.format(type(keyless))
	else:
		checks = ()
	return next(ExtendedFilter(members, *checks, **attrs))

@command
def members(ctx, keyless=None, all=True, **attrs):
	members = list(ctx.guild.members)
	if all: members.extend(ctx.bot.get_all_members())
	if isinstance(keyless, int):
		attrs['id'] = keyless
		checks = ()
	elif isinstance(keyless, str):
		checks = (lambda mem: keyless in (mem.name, str(mem), mem.display_name),)
	elif keyless is not None:
		return 'Unable to infer key from {0.module.__name__}.{0.__qualname__}'.format(type(keyless))
	else:
		checks = ()
	return list(ExtendedFilter(members, *checks, **attrs))

@command
def channel(ctx, keyless=None, all=True, **attrs):
	return next(find(ctx.guild.channels, all and ctx.bot.get_all_channels(), keyless, attrs))

@command
def channels(ctx, keyless=None, all=True, **attrs):
	return list(find(ctx.guild.channels, all and ctx.bot.get_all_channels(), keyless, attrs))

@command
def role(ctx, keyless=None, all=True, **attrs):
	return next(find(ctx.guild.roles, all and itertools.chain.from_iterable(g.roles for g in ctx.bot.guilds), keyless, attrs))

@command
def roles(ctx, keyless=None, all=True, **attrs):
	return list(find(ctx.guild.roles, all and itertools.chain.from_iterable(g.roles for g in ctx.bot.guilds), keyless, attrs))

@command
def emoji(ctx, keyless=None, all=True, **attrs):
	return next(find(ctx.guild.emojis, all and itertools.chain.from_iterable(g.emojis for g in ctx.bot.guilds), keyless, attrs))

@command
def emojis(ctx, keyless=None, all=True, **attrs):
	return list(find(ctx.guild.emojis, all and itertools.chain.from_iterable(g.emojis for g in ctx.bot.guilds), keyless, attrs))

@command
def guild(ctx, keyless=None, **attrs):
	return next(find(ctx.bot.guilds, None, keyless, attrs))

@command
def guilds(ctx, keyless=None, all=True, **attrs):
	return list(find(ctx.bot.guilds, None, keyless, attrs))

def find(limited_list, all_list, keyless, attrs):
	candidates = list(limited_list)
	if all_list: candidates.extend(all_list)
	if isinstance(keyless, int):
		attrs['id'] = keyless
	elif isinstance(keyless, str):
		attrs['name'] = keyless
	elif keyless is not None:
		return 'Unable to infer key from {0.module.__name__}.{0.__qualname__}'.format(type(keyless))
	return ExtendedFilter(candidates, **attrs)

class ExtendedFilter(Iterator):
	def __init__(self, itr, *checks, **attrs):
		self._itr = iter(itr)
		self._checks = checks
		self._attrs = attrs
	
	def check(self, obj):
		if not all(check(obj) for check in self._checks):
			return False
		for name, value in self._attrs.items():
			try:
				if functools.reduce(getattr, name.split('__'), obj) != value: # 'attr1__attr2__attr3' becomes obj.attr1.attr2.attr3
					return False
			except AttributeError:
				return False
		return True
	
	def __next__(self):
		while True:
			obj = next(self._itr) # Let StopIterations get raised
			if self.check(obj):
				return obj
