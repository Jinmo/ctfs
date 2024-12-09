import json
from web3 import Web3
from pwn import *

import string

r = remote(args.get('HOST', "localhost"), args.get('PORT', 9256))

r.recvuntil(b"action? ")
r.sendline(b"1")

r.recvuntil(b"prefix:")
prefix = r.recvline().strip().decode()
r.recvuntil(b"difficulty:")
difficulty = int(r.recvline().strip().decode())
TARGET = 2 ** (256 - difficulty)
alphabet = string.ascii_letters + string.digits + "+/"
answer = iters.bruteforce(
    lambda x: int.from_bytes(util.hashes.sha256sum((prefix + x).encode()), "big")
    < TARGET,
    alphabet,
    length=7,
)
r.sendlineafter(b">", answer.encode())

r.recvuntil(b"token:")
token = r.recvline().strip()
print(f"Token: {token}")
r.recvuntil(b"rpc endpoint:")
rpc_url = r.recvline().strip().decode()
print(f"URL: {rpc_url}")
print(f"RPC endpoint: {rpc_url}")
r.recvuntil(b"private key:")
privk = r.recvline().strip().decode()
r.recvuntil(b"challenge contract:")
challenge_addr = r.recvline().strip().decode()
print(f"Challenge: {challenge_addr}")

w3 = Web3(Web3.HTTPProvider(rpc_url))

# Create smart contract instance
w3.eth.send_transaction({
    'to': challenge_addr,
    'from': w3.eth.accounts[0], # == owner
    'data': '0x890d6908' # cast sig 'solve()'
})
