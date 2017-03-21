from inspect import isgenerator

handlers = {}
general_prefix = 'S+'
def handler(prefix): # This function returns the decorator
	def registrar(fn): # The decorator
		handlers[general_prefix + prefix] = fn
		return fn # No need to edit the function
	return registrar

def handle_message(client, message):
	if message.author != client.user: return
	for prefix in handlers:
		if message.content.startswith(prefix):
			print('Delegating "%s" to %s' % (message.content, handlers[prefix].__name__))
			message_content = message.content[len(prefix):].strip()
			ret = handlers[prefix](client, message, message_content)
			delete = True
			if isgenerator(ret):
				gen = Generator(ret)
				yield from gen
				delete = gen.value
			else: delete = ret
			if delete is not False: yield from client.delete_message(message)
			return

# http://stackoverflow.com/a/34073559
class Generator:
	def __init__(self, gen):
		self.gen = gen
	
	def __iter__(self):
		self.value = yield from self.gen
