import asyncio, discord, inspect, itertools, operator, re, traceback

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
		if code.startswith('```'): # Remove multiline code blocks
			self.code = code.strip('```').partition('\n')[2].strip()
		else: # Remove single-line code blocks, if necessary
			self.code = code.strip('`').strip()
	
	async def invoke(self, ctx):
		locals_ = locals().copy()
		try:
			load_function(self.code, dict(globals(), **ctx.bot.commands), locals_)
		except SyntaxError as err:
			traceback.print_exception(type(err), err, err.__traceback__)
			return 'SyntaxError: %s' % err
		
		try:
			ret = await locals_['evaluation'](ctx)
			if asyncio.iscoroutine(ret):
				ret = await ret
			elif ret in ctx.bot.commands.values():
				ret = await ret()
		except Exception as err:
			traceback.print_exception(type(err), err, err.__traceback__)
			return '%s: %s' % (type(err).__name__, err)
		else:
			return str(ret)

def load_function(code, globals_, locals_):
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
		exec(function_header + line_sep + line_sep.join(lines), globals_, locals_)
	else:
		try:
			exec(function_header + '\n\treturn ' + lines[0], globals_, locals_)
		except SyntaxError as err: # Either adding the 'return' caused an error, or it's user error
			if err.text[err.offset-1] == '=' or err.text[err.offset-3:err.offset] == 'del' or err.text[err.offset-6:err.offset] == 'return': # return-caused error
				exec(function_header + '\n\t' + lines[0], globals_, locals_)
			else: # user error
				raise err
