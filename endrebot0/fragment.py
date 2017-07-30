import asyncio, discord, inspect, re

__all__ = ['fragment']

_pattern = re.compile(r'\{\{[^\}]*\}\}')

def fragment(content):
	code_fragments = _pattern.findall(content)
	idx = 0
	for frag in code_fragments:
		frag_start = content.find(frag, idx)
		if frag_start != idx: yield TextFragment(content[idx:frag_start])
		yield CommandFragment(frag)
		idx = frag_start + len(frag)
	if idx < len(content):
		yield TextFragment(content[idx:]) # This will only be text

class Fragment:
	def __init__(self, content):
		self.content = content
	
	def __str__(self):
		return '%s[%s]' % (self.__class__.__name__, self.content)
	
	def __repr__(self):
		return '%s[%s]' % (self.__class__.__name__, repr(self.content))

class TextFragment(Fragment):
	async def invoke(self, ctx):
		return self.content

class CommandFragment(Fragment):
	async def invoke(self, ctx):
		cmd = self.content[2:-2].strip()
		code = create_function(cmd)
		locals_ = locals()
		globals_ = dict(globals(), **ctx.bot.commands)
		
		try:
			exec(code, globals_, locals_)
		except SyntaxError as err:
			return 'SyntaxError: %s' % err
		
		try:
			ret = await locals_['evaluation'](ctx)
			if asyncio.iscoroutine(ret):
				ret = await ret
			elif ret in ctx.bot.commands.values():
				ret = await ret()
		except Exception as err:
			return '%s: %s' % (type(err).__name__, err)
		
		return ret if ret is None else str(ret)

def create_function(code):
	if code.startswith('```'): code = code[code.find('\n'):code.rfind('\n')].strip() # Remove multiline code blocks
	elif code.startswith('`'): code = code[1:-1].strip() # Remove single-line code blocks
	
	function_header = 'async def evaluation(ctx):'
	
	lines = code.splitlines()
	if len(lines) > 1:
		indent = 4
		for line in lines:
			line_indent = re.search(r'\S', line).start() # First non-WS character is length of indent
			if line_indent:
				indent = line_indent
				break
		line_sep = '\n' + ' ' * indent
		return function_header + line_sep + line_sep.join(lines)
	elif code.startswith(('return', 'del')) or '=' in code:
		return function_header + '\n    ' + code
	else:
		return function_header + '\n    return ' + code
