from ctypes import cdll
import time

from Crypto.Cipher import AES
from Crypto.Util import Counter

libc = getattr(cdll, 'libc.so.6')
srand = libc.srand
rand = libc.rand

target='\x1e\x60\x48'
key = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz"
ts=int(1552348799)
r32 = range(32)

data=open('temp.bin','rb').read()

while True:
    ctr = Counter.new(128, initial_value=0xe4b8c75accb877dab0f5a6f0a7aa0e67)
    srand(ts)
    s = ''.join(key[rand()%0x3e] for i in r32)
    aes = AES.new(s, AES.MODE_CTR, counter=ctr)
    x = aes.encrypt('// ')
    if x==target:
        ctr = Counter.new(128, initial_value=0xe4b8c75accb877dab0f5a6f0a7aa0e67)
        aes = AES.new(s, AES.MODE_CTR, counter=ctr)
        print aes.decrypt(data)
        print ts
        break
    ts += 1

