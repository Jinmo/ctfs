from hashlib import md5

i = 0
while True:
	s = md5(str(i).ljust(32)).hexdigest()
	if s.startswith('0e') and unicode(s[2:]).isnumeric():
		print i
		exit()
	i += 1

# 839284695
