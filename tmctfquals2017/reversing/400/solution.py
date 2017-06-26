import struct

def rand():
	global seed
	seed = 214013 * seed + 2531011;
	seed &= 0xffffffff
	return (seed >> 16) & 0x7FFF;

ror = lambda val, r_bits, max_bits: \
    ((val & (2**max_bits-1)) >> r_bits%max_bits) | \
    (val << (max_bits-(r_bits%max_bits)) & (2**max_bits-1))

seed = 4919
s = bytearray('0p3n5354m3...=.=')
k = 'n\xc2\xe1-\x05\xf8hq\xafvh\xfd\xf8v\xa3\x82'

v6 = 0x12345678
r = []
for i in range(13):
	r.append(v6)
	v8 = ror(v6, 5, 32)
	v6 = rand() % 13371337 ^ v8
print map(hex, r)
for i in range(13):
	j = 12 - i
	s[j:j+4] = struct.pack("<L", r.pop() ^ struct.unpack("<L", str(s[j:j+4]))[0])
	s[j] = ror(s[j], 3, 8)

s = bytearray([(x)^ord(y) for x, y in zip(s, k)])
print `s`