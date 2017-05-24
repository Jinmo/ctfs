key = "OSWMxhJGsIX2jEB7"
p = [11, 15, 14, 13, 7, 9, 6, 3, 0, 1, 2, 10, 5, 12, 8, 4] # from key?
invp = [None] * len(p)
for i in range(len(p)):
	invp[p[i]] = i
input = 'Abcdefghijklmno'
input = bytearray(input)
sum = 0
def rand(n):
	while True:
		n = (123 * n + 59) % 65536
		yield n
for i in range(len(input)):
	d = i + 1
	if i % 2:
		d = -d
	sum += input[i] + d
	print sum

print sum
R = rand(sum % 256)

input = bytearray(str(input).encode('rot13'))
input += '\x00' * (16 - len(input) % 16)
input = [input[p[i]] for i in range(16)]
print input
input = [x^y&0xff for x, y in zip(input, R)] + [sum % 256 ^ 66]
print input
input = str(bytearray(input)).encode('hex')
print input

t = "fc55e53d4bee0c96a781e1cffe7f3dce433242df298f2a97edc235eb191c9da6d22116cdba99beb14ca6d4bd77098e0797"
t = t.decode('hex')
t = bytearray(t)
seed = t.pop() ^ 66
print seed
R = rand(seed)
t = [x^y&0xff for x, y in zip(t, R)]
for i in range(0, len(t), 16):
	t[i:i+16] = [t[i:i+16][invp[j]] for j in range(16)]
t = bytearray(t)
t = str(t).encode('rot13')
t = t.rstrip('\x00')
print t