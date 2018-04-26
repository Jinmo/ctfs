#!/usr/bin/python3
from hashlib import sha256
from itertools import permutations

import string

# Just looked EVM assembly for many hours to solve it.
if False:
	keys = string.ascii_lowercase
	for combs in permutations(keys, 4):
		z = sha256(bytearray(combs)).hexdigest()
		# x = x[::-1]
		if z == hash or z == hash[::-1] or z == bytes.fromhex(hash)[::-1].hex() or z[::-1] == bytes.fromhex(hash)[::-1].hex():
			print(combs)
			exit()

keys = bytearray(bytes.fromhex("4419194e"))
for i in range(len(keys)):
	keys[i] ^= 42

hash = 'a8c8af687609bf404c202ac1378e10cd19421e72c0a161edc56b53752326592a'
prefix = b"flag{mayb3_w3_"
suffix = b"_bett3r_t00ls}"
x = bytearray(prefix + keys + suffix)
print(x)
