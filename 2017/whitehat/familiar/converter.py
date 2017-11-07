import string
import sys

keys = string.uppercase + string.lowercase + string.digits + '+' + '/'

s = sys.stdin.read()
s = ''.join([bin(ord(x))[2:].zfill(16) for x in s])
def decode(x):
	r = ''
	x += '0' * (6 - len(x) % 6)
	for i in range(0, len(x), 6):
		r += keys[int(x[i:i+6], 2)]
	return r
s = '+' + decode(s)
print ''.join(s)
