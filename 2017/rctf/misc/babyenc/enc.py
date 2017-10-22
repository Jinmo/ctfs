import codecs
from z3 import *
def m_simplify(x):
	if type(x) in [long, int]:
		return x
	else:
		return simplify(x)
def enc(s, t):
	if t:
		return enc([m_simplify(s[i]^s[i+1]) for i in range(len(s)-1)], t-1)
	else:
		return s

# a b c d e
#   b c d e f
#     c d e f g
#       d e f g h
#         e f g h i
f = open('out.txt', 'rb')
orig = l = bytearray(f.read().replace('\x0d\x0a', '\x0a'))
size = len(l)
data = l = [BitVec('l[%d]' % i, 8) for i in range(len(l) + 5)]
l = enc(l, 5)
print len(l), size
print l[0]
s = Solver()
blacklist = ''
prefix = 'Make '
for c, d in zip(l, orig):
	s.add(c == d)
for c in data:
	s.add(Or(c > 0))
	for d in blacklist:
		s.add(c != ord(d))
for c, d in zip(data, prefix):
	s.add(c == ord(d))
if s.check() == sat:
	model = s.model()
	flag = [model[data[i]].as_long() for i in range(len(data))]
	print flag
	print `str(bytearray(flag))`
	print enc(bytearray(flag), 5) == list(bytearray(orig))
else:
	print s.check()
exit()
print reduce(lambda x, y: x ^ y, bytearray('RI{e'), 0)
print `l`
exit()
l = bytearray(l)
l = bytearray([l[i]^l[i+1] for i in range(len(l)-1)])
l = bytearray('ROIS{') + l
result = bytearray()
for i in range(5, len(l)):
	result.append(l[i-5] ^ l[i])
# print l
print result
exit()

with open('in.txt') as f:
	s = enc(f.read(), 5)
with open('out.txt', 'w') as f:
	f.write(s)