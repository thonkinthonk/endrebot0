cfg = open('endrebot0.cfg', 'r')
config = {}
for line in cfg:
	ind = line.find(':')
	config[line[:ind]] = line[ind+1:-1] #Remove \n
print('Loaded config', config)
