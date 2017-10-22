flag = [199, 102, 252, 214, 92, 182, 13, 232, 41, 99, 59, 168, 216, 184, 35, 82, 111, 248, 35, 156, 29, 214, 222, 115, 235, 150, 53, 54, 179, 72, 51, 70]
d = eval(open('lights.txt', 'rb').read())
for y in range(0x80):
	for x in range(0x80):
		if d[y * 0x80 + x]:
			flag[16 * (y & 1) + (x >> 3)] ^= 1 << (7 - x & 7)

print bytearray(flag)