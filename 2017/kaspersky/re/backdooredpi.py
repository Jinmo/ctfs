import hashlib

for j in range(1, 9):
	print j
	i = 0
	maxvalue = 10 ** j
	while i < maxvalue:
		text = '{}:{}'.format('b4ckd00r_us3r', ('%0' + str(j) + 'd') % i)
		print text
		if hashlib.sha256(text).hexdigest() == '34c05015de48ef10309963543b4a347b5d3d20bbe2ed462cf226b1cc8fff222e':
			print text
		i += 1