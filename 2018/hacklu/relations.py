from pwn import *

r = remote('arcade.fluxfingers.net', 1821)

cur = 1
def recv():
        r.recvuntil('is  ')
        data = r.recvuntil('-', drop=True)
        return data
result = 0
for i in range(8 * 16):
        r.send('XOR\n%x\n' % cur)
        r.send('ADD\n%x\n' % cur)
        cur <<= 1

cur = 1
for i in range(8 * 16):
        a = recv()
        b = recv()
        print `a`, `b`
        # if nth bit is 0, then xor = add
        print a != b
        result += (a != b) * cur
        print hex(result)
        cur <<= 1

r.send('DEC\n%s\n' % ('%x'%result).decode('hex').encode('base64').replace('\n', ''))
r.interactive()