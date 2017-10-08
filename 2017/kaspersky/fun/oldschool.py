import string
data = open('C:/Users/berry/Downloads/old_school.bin', 'rb').read()
map = data[0x2b93-55:]
known = {
	3: 'W',
	0x11: ' ',
	0x10: '.'
}
for i in range(0, len(map), 55):
	line = map[i:i+55]
	print i / 55, ''.join([x if x in string.digits else known.get(ord(x), '.') for x in line])
	if (i / 55) % 55 == 54:
		for i in range(9):
			print