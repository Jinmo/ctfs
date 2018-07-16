# from https://github.com/pcaro90/Python-AES
from AES import *

key = [
# xor
[0x60, 0x9D, 0x47, 0x31, 0xB5, 0xDD, 0x36, 0x7E, 0xEF, 0x99, 0x7A, 0xD8, 0x49, 0x5C, 0x45, 0x23, ], # exec3
[0xFA, 0xEC, 0xDB, 0xBB, 0x93, 0xB2, 0x3A, 0xEF, 0x68, 0xE4, 0xBE, 0x6D, 0x2F, 0xF6, 0x6B, 0x4C, ], # exec1

[0x3E, 0x43, -107, 60, 105, -48, 115, 103, 34, -105, -47, -79, -93, 97, -3, 74, ], # 2_0
[0x45, 0x33, 0x7E, 0x3C, 0xF0, 0x7F, 0x2D, 0xAC, 0x33, 0x44, 0x3B, 0x75, 0x48, 0x2A, 0xC5, 0x46, ], # 3_0
[77, -16, -20, 26, 61, 4, -87, -37, -11, -43, 8, 26, -128, 112, -109, 6, ], # 1_0

[-70, -16, -85, 31, -84, 47, 88, -127, -15, 37, -79, 89, -7, 121, -34, 3, ], # 2_1
[0x34, -81, -1, 87, 81, 58, 15, -20, -117, -96, -26, 95, -116, -104, 96, 120, ], # 3_1
[0x2E, -21, -49, 70, 5, -82, 61, -108, -70, -116, -52, -12, 76, -95, 29, 76, ], # 1_1

[0x74, -7, -59, 66, 127, 122, 110, -30, 0xB1, 31, 44, -62, 24, 4, -72, -9, ], # 2_2,
[0xA, 0x98, 0x63, 0x1D, 0x84, 0x69, 0x82, 8, 7, 0xCA, 0x31, 0xF7, 0x1D, 0x33, 0x56, 0x29, ], # 3_2
]

_ = lambda f: [x & 0xff for x in f]
xor = lambda x, y: [a ^ b for a, b in zip(bytearray(x), bytearray(y))]
encode = lambda x: process_key(str(bytearray(x)).encode('hex'))

print list((len(x) == 16 for x in key))
key = map(_, key)

target = [0x68, 0xCE, -33, -35, 88, 108, 55, -28, -60, -31, -84, -76, 9, 127, -105, -92, ] # 1_2
target = _(target)

y = target[:]

for i, x in enumerate(key[::-1]):
	y = xor(x, y)
	y = encode(y)
	if i:
		y = InvMixColumns(y)
		y = InvSubBytes(y)
		y = InvShiftRows(y)
	else:
		y = InvSubBytes(y)
		y = InvShiftRows(y)
	y = reduce(lambda x, y: x + y, y, [])

x = 0x6A, 0x15, 0x6D, 0xB, 0x9D, 0xF0, 0xC2, 0x34, 0x74, 0x8A, 0xD4, 0x4F, 0x50, 0x84, 0xA0, 0x7F, 
y = str(bytearray(xor(y, x)))
print `y`