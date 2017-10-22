#!/usr/bin/env python
import os
from Crypto.Cipher import AES
import socket

pad = lambda m: m + str(bytearray([16 - len(m) % 16] * (16 - len(m) % 16)))
l='\x00'*0xf+'\x8f'
while True:
	s = socket.create_connection(('104.198.243.170', 2501))
	target = s.recv(1024).strip()
	target = target.decode('hex')
	# target = os.urandom(16)
	prefix = 'I solemnly swear that I am up to no good.\0'.ljust(128)
	crypt0r = AES.new('\x00'*0x10, AES.MODE_CBC, '\x00' * 16)
	iv=crypt0r.encrypt(l + prefix)[-16:]
	crypt0r = AES.new('\x00'*0x10, AES.MODE_CBC, iv)
	r=prefix + crypt0r.decrypt(target)
	if r[-1] == '\x01':
		print `r`
		r = r[:-1]
		def haggis(m):
		    crypt0r = AES.new('\x00'*0x10, AES.MODE_CBC, '\x00'*0x10)
		    print `pad(m)`
		    return crypt0r.encrypt(l + pad(m))[-0x10:]

		print `haggis(r)`, 1
		print `target`
		print hex(len(r))
		s.send(r.encode('hex') + '\n')
		print s.recv(1024)
		print s.recv(1024)
		break