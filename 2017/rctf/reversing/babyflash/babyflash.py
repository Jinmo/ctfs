s = 'RCTF{_Dyiin9__F1ash__1ike5_CPP}'
v8 = 2
v7 = 3
flag = ''
i = 0
j = 0
while i < len(s):
	flag += s[i]
	v2 = 1
	if j != v8 * 2:
		v2 = 0
	if v2:
		v3 = v7 + v8
		v8 = v7
		v7 = v3
		i += 1
	i += 1
	j += 1

print flag