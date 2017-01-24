from z3 import *
from pwn import *
import struct

key = [3735928559L, 322433024L, 1111638594L, 12648430L] # const

# Rotate left: 0b1001 --> 0b0011
rol = lambda val, r_bits, max_bits=64: \
    (val << r_bits%max_bits) & (2**max_bits-1) | \
    ((val & (2**max_bits-1)) >> (max_bits-(r_bits%max_bits)))
 
# Rotate right: 0b1001 --> 0b1100
ror = lambda val, r_bits, max_bits=64: \
    ((val & (2**max_bits-1)) >> r_bits%max_bits) | \
    (val << (max_bits-(r_bits%max_bits)) & (2**max_bits-1))

b = lambda x: BitVecVal(x, 64)

r = remote('104.197.187.242', 2048)
r.recvline()
r.sendline('L')
for i in range(8):
	print r.recvuntil('-------------------------------------------------')
	data = r.recvuntil('--------------------------------------------------------------------------------', drop=True)
	data = data.decode('base64').decode('zlib')

	f = open('tmpf', 'wb')
	f.write(data)
	f.close()

	elf = ELF('tmpf')
	main = elf.symbols['main']
	target = []
	for needle in elf.search('\x48\xb8'):
		target.append(u64(elf.read(needle + 2, 8)))
	print map(hex, target)
	b1 = b(0L)
	b2 = b(0L)
	b3 = b(0L)
	b4 = b(0L)
	m = [BitVec('M%d' % i, 32) for i in range(4)]
	_ror = ror
	_rol = rol
	ror = RotateRight
	rol = RotateLeft
	for v8 in range(4):
	    c = ZeroExt(32, m[v8 & 0xf])
	    k = key[v8 & 3]
	    b1 = k + (c ^ rol(b1, 13))
	    b2 = (c ^ ror(b2, 13)) - k
	    k <<= 32
	    b3 = k + (c ^ ror(b3, 19))
	    b4 = (rol(b4, 19) ^ c) - k

	s = Solver()
	s.add(b1 == target[0]
	    ,b2 == target[1]
	    ,b3 == target[2]
	    ,b4 == target[3])

	s.check()
	model = s.model()
	m = [model[x].as_long() for x in m]

	b1 = b2 = b3 = b4 = 0
	mask = 0xffffffffffffffff
	ror, rol = _ror, _rol
	for v8 in range(4):
	    c = m[v8 & 0xf]
	    k = key[v8 & 3]
	    b1 = k + (c ^ rol(b1, 13))
	    b2 = (c ^ ror(b2, 13)) - k
	    k <<= 32
	    b3 = k + (c ^ ror(b3, 19))
	    b4 = (rol(b4, 19) ^ c) - k
	    b1 &= mask
	    b2 &= mask
	    b3 &= mask
	    b4 &= mask

	print hex(b1), hex(b2), hex(b3), hex(b4)
	result = struct.pack("<4L", *m).encode('base64').replace('\n', '')
	print result
	r.sendline(result)

r.interactive()