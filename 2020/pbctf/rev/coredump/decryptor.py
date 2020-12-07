import hashlib
from randlib import Context, decrypt
from pwn import *
rng = Context(0xb1584c802e81d67 & 0xffffffff)
data = open('flag.enc', 'rb').read()
cnt = rng.generate() & 0xfff
a = bytearray(b'|\xa1\xdc\t\x86\x93\x9b\xa5\x96\xbcu\xd68TQ\xa9\xe3T\xb7\\lF\xc8\t\xfd\xab/\x11\x1a\x8dp\xb6D\xee\xd8h\xa54\x86\xf6O\x1c\xb4\x03>fm\xce(\xa2G\x95\xe40J\xa9\xeb\xb6\x88\xe4Gz\xd5\x9a\xd8\xa9R>\x9f\xae\x80l\xablO\xb7\x9a\xc7viUEhK\x10IA\x90n\x13\x89\xf4g\xbe\x8a\xd5\x07\x82\x15K')
for i in range(cnt):
    for j in range(100):
        a[j] ^= rng.generate() & 0xff
print(a)
pw = b'mypassword_is_secure!!'.ljust(100, b'\x00')
print(hexdump(a))
r = a.index(0)
a = decrypt(bytes([x ^ y for x, y in zip(a, pw)]), 0x843)[:r] + a[r:]
print(a)
print(bytes(x ^ y for x, y in zip(data, hashlib.sha256(a).digest())))
