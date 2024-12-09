import json
from web3 import Web3
from pwn import *

import string

r = remote(args.get('HOST', "localhost"), args.get('PORT', 9035))

r.recvuntil(b"prefix:")
prefix = r.recvline().strip().decode()
r.recvuntil(b"difficulty:")
difficulty = int(r.recvline().strip().decode())
TARGET = 2 ** (256 - difficulty)
alphabet = string.ascii_letters + string.digits + "+/"
answer = os.popen(f'~/pow/target/release/pow {prefix}').read().strip()
r.sendlineafter(b">", answer.encode())

r.recvuntil(b'pls')
r.sendline(base64.b64encode(open('service/exploit', 'rb').read()))
r.interactive()
