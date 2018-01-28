from z3 import *
import struct
dword_250 = [BitVec('x[%d]' % i, 32) for i in range(9)]
s = Solver()
s.add(dword_250[1] + dword_250[0] == 0x81888E82,
dword_250[0] - dword_250[1] == 0xFFFC00,
dword_250[3] + dword_250[2] == 0x868C8682,
dword_250[2] - dword_250[3] == 0xF9F9FC00,
dword_250[5] + dword_250[4] == 0x8A85898F,
dword_250[4] - dword_250[5] == 0x804FAFD,
dword_250[7] + dword_250[6] == 0x89858989,
dword_250[6] - dword_250[7] == 0x7030901,
dword_250[8] == 0x43494545)
s.check()
data = [s.model()[dword_250[i]].as_long() for i in range(len(dword_250))]
data += [1094797125L, 1229013065L, 1078018368L, 1094796353L, 1229211972L]
data = [struct.pack("<L", data[i]) for i in range(len(data))]
def extract(x):
	x = [(ord(y)-0x30)^0x10 for y in x]
	return ''.join(str(y) for y in x)
data = map(extract, data)
print data
data = map(str, data)
data = ''.join(data)
print data
print extract('F@AE')















print data
c = ''
# I manually reversed each decimal ascii character, but for explanation, I put it as code
i = 0
flag = []
while i < len(data):
	c += data[i]
	if len(c) > 2 and data[i] == '0':
		flag.append(c[:-1][::-1])
		c = c[-1]
		i += 1
		c += data[i]
	if int(c[::-1]) > 128:
		flag.append(c[:-1][::-1])
		c = c[-1]
	i += 1
print bytearray(map(int, flag))
print