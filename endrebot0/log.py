import logging, sys

def _logger(name, outs):
	logger = logging.getLogger(name)
	logger.setLevel(min(outs.values()))
	
	for out, level in outs.items():
		handler = logging.FileHandler(filename=out, encoding='utf-8', mode='w') if isinstance(out, str) else logging.StreamHandler(out)
		handler.setLevel(level)
		handler.setFormatter(logging.Formatter('[%(asctime)s] [%(levelname)s] [%(name)s] %(message)s'))
		logger.addHandler(handler)
	return logger

root = _logger('', {'logs/all': logging.INFO})
discord = _logger('discord', {'logs/discordpy': logging.INFO})
main = _logger('endrebot0', {'logs/endrebot0': logging.DEBUG, sys.stdout: logging.INFO})

module = sys.modules[__name__]
for level in ('debug', 'info', 'warn', 'error', 'critical', 'fatal'):
	setattr(module, level, getattr(main, level))

shutdown = logging.shutdown
