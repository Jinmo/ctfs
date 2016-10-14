from pwn import *

HOST, PORT = 'challenges.hackover.h4q.it', 4242
r = remote(HOST, PORT)

r.recvuntil(': ')
r.sendline('ngngzudxirxb')
r.recvuntil(': ')
r.send('4028460962406821846280430684026')
r.interactive()