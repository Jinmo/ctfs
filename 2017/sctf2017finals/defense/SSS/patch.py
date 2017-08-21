import socket
import json

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect(('sss.EatpwnNoSleep.com', 18878))
YOUR_API_KEY = '43073909ecc48af12aa63c8f74989bc9523587eca49d37c97edd3027984e6101'

a = {
    'apikey' : YOUR_API_KEY,
}

s.send(json.dumps(a).encode())
print (s.recv(102400))

for path in 'valcell.c', 'valenv.c':
	for i in range(2):
		print s.recv(102400)

	s.send(path + '\n')

	print s.recv(102400)
	s.send(open(path, 'rb').read().encode('base64').replace('\n', '') + '\n')

for i in range(2):
	print s.recv(102400)

s.send('finish\n')

for i in range(100):
	c = s.recv(102400)
	if c == '':
		break
	print c