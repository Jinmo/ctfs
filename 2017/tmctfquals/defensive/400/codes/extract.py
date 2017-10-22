from json import load
from itertools import cycle

j = load(open('../extractme2.json', 'r'))
def parse(x):
	return x.replace(':', '').decode('hex')
file = open('output', 'wb')
key = None
for p in j:
	if 'smb' in p['_source']['layers']:
		smb = p['_source']['layers']['smb']
		if 'Trans2 Request (0x32)' in smb:
			trans = smb['Trans2 Request (0x32)']
			if 'SESSION_SETUP Parameters' in trans:
				data = parse(trans['SESSION_SETUP Parameters']['smb.unknown_data'])
				if key is None and data.strip('\x00') != '':
					key = data[8:12]
			if 'SESSION_SETUP Data' in trans:
				data = trans['SESSION_SETUP Data']['smb.unknown_data']
				data = bytearray([ord(x)^ord(y) for x, y in zip(parse(data), cycle(key))])
				print len(data)
				file.write(data)