import socket
from multiprocessing import Pool

sock = lambda: socket.create_connection(('128.199.128.238', 31333))

def send(text):
	s = sock()
	s.send('GET /login/%s' % str(text).encode('hex') + '\n')
	data = ''
	while True:
		c = s.recv(1024)
		if c == '':
			break

		data += c

	return data

def run(args):
	i, j, text = args
	text[j] = i
	data = send(text)


	if 'line 2 column' in data:
		print data
		return 1
	else:
		return 0

if __name__ == '__main__':
	keys = [0] * 16
	Pool = Pool(8)
	text = bytearray('\x00' * 16)
	text[0] = keys[0] ^ 0x31
	for j in range(0, 16):
		map = Pool.map(run, [(i, j, text) for i in range(256)])
		print map
		key = None
		for i in range(256):
			if map[0x22 ^ i] == 1:
				key = i
				break
		if key is None:
			print 'wtf'
			exit()
		print key,
		keys[j] = key
		print keys
		if j == 0:
			text[j] = key ^ 0x31
		else:
			text[j] = key ^ 0x31

	text = '{"user":"admin"}'
	text = bytearray(text)
	for i in range(len(text)):
		text[i] ^= keys[i]

	send(text)