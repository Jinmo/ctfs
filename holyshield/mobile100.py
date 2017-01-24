from itertools import permutations
import hashlib

array = [12,
16,
78,
95,
64,
75,
67,
92,
10,
45,
61,
33,
23,
58,
89,
77]

key = '1mh2fedclpib3qjo'
original = 'abcdefghijlmnopq'
k = 'agn'
for a, b, c in permutations((0, 1, 2), 3):
	cc = key.replace('1', k[a]).replace('2', k[b]).replace('3', k[c])

	result = ''
	for c in cc:
		result += str(array[original.index(c)])

	# print result
	print hashlib.md5(result).hexdigest(), result