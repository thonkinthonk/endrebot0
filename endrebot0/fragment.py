import asyncio, discord, inspect, itertools, operator, re

__all__ = ['Fragmenter']

def strfind(str_, subs, *find_args):
	inds = [tup for tup in ((sub, str_.find(sub, *find_args)) for sub in subs) if tup[1] >= 0]
	return min(inds, key=operator.itemgetter(1)) if inds else ('', -1)

class Fragmenter:
	def __init__(self, fragment_start, fragment_end):
		self.start = fragment_start
		self.end = fragment_end
	
	def __call__(self, content):
		idx, start, end = 0, 0, 0
		stack_height = 0
		while idx < len(content):
			match, end = strfind(content, (self.start, self.end), idx)
			if end == -1:
				yield TextFragment(content[idx:])
				break
			if match == self.start:
				if not stack_height:
					if idx != end: yield TextFragment(content[idx:end])
					start = end
				stack_height += 1
			else:
				stack_height -= 1
				if not stack_height:
					yield CommandFragment(content[start:end+len(match)], content[start+len(self.start):end])
			idx = end + len(match)

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
	def __init__(self, content, code):
		super().__init__(content)
		self.code = code.strip()
	
	async def invoke(self, ctx):
		code = create_function(self.code)
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
