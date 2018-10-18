import sys

r = ''
for line in list(open(sys.argv[1], 'rb'))[4::3]:
	r += line.strip()[-1]

flag = ''
print r
for i in range(0, len(r), 8):
	flag += chr(int(r[i:i+8][::-1], 2))
	print flag