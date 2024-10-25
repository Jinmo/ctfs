target = b'\xbf\x96\xaaF\x11#k\xb2s^\\TFTBBTXNRSSM\x1e`\x07."#e/4hn\t\x1f\n6\x16\x17\x08,us#=3%=y\x02\x03\x04}7,@\x18\r\x16\x16E\x0f\t\x18\x1c\x1eEf9\x1c\x16P\x10\x15\x12\x1d\x1bW}'
orig = target
for j in range(256):
	pc = j
	target = list(orig)
	for i in range(0x50):
		target[i] ^= pc & 0xff
		pc += 1
	if b'Congratulations' in bytes(target):
		print(hex(j), bytes(target))
