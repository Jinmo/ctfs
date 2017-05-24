import string

m4 = lambda x, y: x + y
m1 = lambda x, y: x % y
m2 = lambda x, y: x * y
m3 = lambda x, y: x % y
m5 = lambda x, y: x ^ y

codes = bytearray("a#s224kfuSaom=D469asSkOdhmP34!@-")

def box1to1(s):
	s = list(s)
	s = [x % 10 for x in s]
	r = list()
	for i in range(32):
		a = m3(i, len(s))
		b = m3(i, len(codes))
		c = m4(b, s[a])
		d = m1(c, codes[b])
		e = m2(c, d)
		f = m5(d, codes[a])
		g = m4(e, f)
		r.append(g & 0xff)
	return r

def merge(a, b):
	a = list(a)
	b = list(b)
	b = [(x / 10) % 10 for x in b]
	result = []
	for i in range(32):
		result.append((b[i % len(b)] + a[i]) % 16)
	return result

hexchars = "0123456789ABCDEF"
def encode(x):
	return ''.join(hexchars[a] for a in x)

charset = string.lowercase + string.uppercase + string.digits + '_-+'
box = {}
for a in charset:
	for b in charset:
		for c in charset:
			s = bytearray([a, b, c])
			text = encode(merge(box1to1(s), s))
			if text not in box:
				box[text] = []
			box[text].append(s)
angry = "6F50D5057EFB2B9411C1B237E7D8588D", "98DD67FE3789D499AB3AF3CD1055EB76", "10556D767F835C91A9B2BBCF98DDE4FE", "72AD4A98C3603EE1865407ACFA25C210"
flag = ''
for s in angry:
	c = box.get(s)
	print c
	if c:
		flag += c[0]

print 'RCTF{' + flag + '}'