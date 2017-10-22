from z3 import *
import itertools
s = 'jinmo123'
s = ''.join([bin(ord(c))[2:].zfill(8) for c in s])
s = [int(c) for c in s]
s = [BitVec('s[%d]' % i, 1) for i in range(64)]
target = [7, 0, 4, 5, 4, 7, 7, 0, 4, 2, 0, 6, 6, 3, 4, 5, 4, 0, 3, 6, 1, 0, 6, 1, 7, 2, 0, 6, 1, 7, 5, 3, 4, 2, 0, 6, 1, 0, 1, 5, 6, 3, 4, 5, 4, 7, 7, 7, 7, 0, 4, 5, 4, 0, 3, 1, 5, 6, 3, 3, 6, 6, 4, 7]
a = [0] * 4
r = []
# Concat = lambda x, y, z: (x << 2) | (y << 1) | z
for c in s:
	a = [0] + a[:3]
	a[0] = c
	# print a
	r.append((Concat((a[0] ^ 1), ((a[1] ^ a[2] ^ a[3] ^ 1 ^ a[0])), ((a[3] ^ a[1] ^ a[0] ^ 1)))))

print len(r)
# print map(bin, r)
# print r
ss = Solver()
for i in range(64):
	ss.add(r[i] == target[i])
if ss.check() == sat:
	s = [ss.model()[s[i]].as_long() for i in range(64)]
#	print s
	id = bytearray()
	for i in range(0, 64, 8):
		id.append(int(''.join([str(c) for c in s[i:i+8]]), 2))
	print id
	pw = [18, 86, 46, 27, 92, 52, 106, 93, 115, 41, 15, 91, 28, 103, 52, 111, 17, 80, 30, 58, 25, 112, 53, 84, 63, 69, 45, 71, 46]
	pw = bytearray([x ^ y for x, y in zip(itertools.cycle(id), pw)])
	print pw
else:
	print 'unsat'