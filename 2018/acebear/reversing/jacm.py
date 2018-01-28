# I MAKE LOT OF GUESSWORKS reversing some platforms
# like rust, swift, go, ...
# I hope all low-level stuffs for these platforms get documented well..

string = '''
allocateUninitializedArraySayxG_BptBwlF(1i64, v32);
42
1
allocateUninitializedArraySayxG_BptBwlF(1i64, v333);
36
1
allocateUninitializedArraySayxG_BptBwlF(2i64, v333);
2
1
10
1
allocateUninitializedArraySayxG_BptBwlF(3i64, v333);
2
1
0
1
7
1
allocateUninitializedArraySayxG_BptBwlF(2i64, v333);
2
1
10
1
allocateUninitializedArraySayxG_BptBwlF(2i64, v333);
15
1
1
1
allocateUninitializedArraySayxG_BptBwlF(2i64, v333);
0
1
19
1
allocateUninitializedArraySayxG_BptBwlF(2i64, v333);
3
1
7
1
allocateUninitializedArraySayxG_BptBwlF(1i64, v333);
35
1
allocateUninitializedArraySayxG_BptBwlF(2i64, v333);
3
1
8
1
allocateUninitializedArraySayxG_BptBwlF(2i64, v333);
3
2
1
1
allocateUninitializedArraySayxG_BptBwlF(2i64, v333);
1
2
8
1
allocateUninitializedArraySayxG_BptBwlF(2i64, v333);
1
1
14
1
allocateUninitializedArraySayxG_BptBwlF(2i64, v333);
1
1
14
1
allocateUninitializedArraySayxG_BptBwlF(2i64, v333);
3
1
8
1
allocateUninitializedArraySayxG_BptBwlF(3i64, v333);
2
1
0
2
3
1
allocateUninitializedArraySayxG_BptBwlF(2i64, v333);
0
3
7
1
allocateUninitializedArraySayxG_BptBwlF(2i64, v333);
2
1
12
1
allocateUninitializedArraySayxG_BptBwlF(2i64, v333);
3
1
8
1
allocateUninitializedArraySayxG_BptBwlF(2i64, v333);
5
1
0
4
allocateUninitializedArraySayxG_BptBwlF(2i64, v333);
0
2
11
1
allocateUninitializedArraySayxG_BptBwlF(3i64, v333);
5
1
0
2
1
1
allocateUninitializedArraySayxG_BptBwlF(2i64, v333);
3
1
8
1
allocateUninitializedArraySayxG_BptBwlF(2i64, v333);
0
2
13
1
allocateUninitializedArraySayxG_BptBwlF(3i64, v333);
6
1
0
2
1
1
allocateUninitializedArraySayxG_BptBwlF(2i64, v333);
2
1
1
3
allocateUninitializedArraySayxG_BptBwlF(2i64, v333);
0
2
11
1
allocateUninitializedArraySayxG_BptBwlF(2i64, v333);
5
1
0
4
allocateUninitializedArraySayxG_BptBwlF(2i64, v333);
0
1
19
1
allocateUninitializedArraySayxG_BptBwlF(2i64, v333);
3
1
8
1
allocateUninitializedArraySayxG_BptBwlF(3i64, v333);
0
1
1
2
4
1
allocateUninitializedArraySayxG_BptBwlF(2i64, v333);
3
1
10
1
allocateUninitializedArraySayxG_BptBwlF(2i64, v333);
0
3
1
3
allocateUninitializedArraySayxG_BptBwlF(1i64, v333);
31
1
'''.strip().split('\n')

r = []
R = None
for line in string:
	if 'allocate' in line:
		data = int(line.split('(')[1].split('i')[0])
		if R: r.append(R)
		R = []
	else:
		R.append(int(line))
primes = [2L, 3L, 5L, 7L, 11L, 13L, 17L, 19L, 23L, 29L, 31L, 37L, 41L, 43L, 47L, 53L, 59L, 61L, 67L, 71L, 73L, 79L, 83L, 89L, 97L, 101L, 103L, 107L, 109L, 113L, 127L, 131L, 137L, 139L, 149L, 151L, 157L, 163L, 167L, 173L, 179L, 181L, 191L, 193L, 197L, 199L, 211L, 223L, 227L, 229L, 233L, 239L, 241L, 251L]
flag = []
for i, x in enumerate(r):
	value = 1
	for j, a, b in zip(range(1000), x[::2], x[1::2]):
		value *= primes[a] ** b
		print i, a, primes[a], b, value
	flag.append(256-value)


flag += [ord('}')] #where it is?
print flag
print bytearray(flag)