import socket
import struct
import sys
from Crypto.Cipher import AES

HOST, PORT = 'challenges.hackover.h4q.it', 1415
s = socket.create_connection((HOST, PORT))

def rw(t):
	d = ''
	while t not in d:
		c = s.recv(1)
		if c == '':
			print 'Socket Error'
			exit()

		sys.stdout.write(c)
		d += c
	return d

def decrypt(text, key):
	aes = AES.new(key)
	return struct.unpack(">H", aes.decrypt(text)[:2])[0]

for i in range(32):
	rw('My dice roll: ')
	enc = rw('\n').decode('base64')
	payload = '\x00' * 16
	rw(': ')
	s.send(payload.encode('base64').replace('\n', '') + '\n')
	rw(': ')
	targetkey = rw('\n').decode('base64')

	r = decrypt(enc, targetkey)
	tr = 7 - r
	target = struct.pack(">H", tr)

	i = 0
	while True:
		key = str(i).ljust(16, "A")
		aes = AES.new(key)
		plaintext = aes.decrypt(payload)
		if plaintext.startswith(target):
			break

		i += 1

	s.send(key.encode('base64').replace('\n', '') + '\n')

while True:
	c = s.recv(1)
	if c == '':
		break

	sys.stdout.write(c)