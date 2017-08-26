from collections.abc import Iterator
from discord.utils import get
from ..command import *

@command
def getone(ctx, itr, check=None, **attrs):
	return next(ExtendedFilter(itr, check, attrs), None)

@command
def getall(ctx, itr, check=None, **attrs):
	return list(ExtendedFilter(itr, check, attrs))

class ExtendedFilter(Iterator):
	def __init__(self, itr, check, attrs):
		self._itr = iter(itr)
		self._check = check
		self._attrs = attrs
	
	def check(self, obj):
		if self._check is not None and not self._check(obj):
			return False
		for name, value in self._attrs.items():
			try:
				if self._get_attr(obj, name) != value:
					return False
			except AttributeError:
				return False
		return True
	
	def _get_attr(self, obj, full_key):
		keys = full_key.split('__')
		for key in keys:
			obj = getattr(obj, key)
		return obj
	
	def __next__(self):
		while True:
			obj = next(self._itr) # Let StopIterations get raised
			if self.check(obj):
				return obj
