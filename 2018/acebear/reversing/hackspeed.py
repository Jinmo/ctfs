from ctypes import *
import struct

libc = CDLL('ucrtbase')
rands = []
for i in range(256):
	libc.srand(i + 1)
	rands.append(libc.rand() & 0xff)

R = list(bytearray('0123456789abcdefghijklmnopqrstuvwxyz'))
r = set(R)
l = list(bytearray(struct.pack("<LLLL", 0xF8E3E7F6, 0x1D16E3DD, 0xCCECECE6, 0x7E9E0E7)))
sort = 'b865d1eca7f94320'
sort = [int(x, 16) for x in sort]
count = 0
for i0 in R:
	i1 = i0 ^ 4
	i2 = i0 ^ 3
	if i1 not in r or i2 not in r:
		continue
	if i0 ^ rands[i0] != l[0]:
		continue
	for i3 in R:
		i4 = i3 ^ 8
		if i4 not in r:
			continue
		if i3 ^ rands[i3] != l[3]:
			continue
		for i5 in R:
			i6 = i5 ^ 80
			if i6 not in r:
				continue
			if i5 ^ rands[i5] != l[5]:
				continue
			for i9 in R:
				i10 = i9 ^ 25
				i12 = i9 ^ 27
				if i10 not in r or i12 not in r:
					continue
				if i10 ^ rands[i10] != l[10]:
					continue
				for i7 in R:
					if i7 ^ rands[i7] != l[7]:
						continue
					for i8 in R:
						if i8 ^ rands[i8] != l[8]:
							continue
						for i13 in R:
							if i13 ^ rands[i13] != l[13]:
								continue
							for i14 in R:
								if i14 ^ rands[i14] != l[14]:
									continue
								for i15 in R:
									if i15 ^ rands[i15] != l[15]:
										continue
									for i11 in R:
										if i11 ^ rands[i11] != l[11]:
											continue
										x = i0, i1, i2, i3, i4, i5, i6, i7, i8, i9, i10, i11, i12, i13, i14, i15
										count += 1
										x = {sort[i]: x[i] for i in range(16)}
										print 'Possible solution:', bytearray(x[i] for i in range(16))
print count