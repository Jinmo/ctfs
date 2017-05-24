import string
import textwrap
d = open('C:/Users/berry/Downloads/msg.txt', 'rb').read()
for j in range(256):
	s = bytearray([(-x+j)%256 for x in bytearray(d)])
	s = str(s)
	print j, `''.join(filter(lambda x: x in string.printable, s))`
	if 'rctf' in s.lower() or 'flag' in s.lower():
		print 'yes'
		exit()
d = d.encode('hex')
d = int(d, 16)
d = bin(d)[2:]
for j in range(5, 800):
	if len(d) % j == 0:
		s = '\n'.join(textwrap.wrap(d, j))
		s = s.replace('0', ' ')
		print s
exit()
print len(d)
print `bytearray([int(d[i:i+3], 2)+48 for i in range(0, len(d), 7)])`