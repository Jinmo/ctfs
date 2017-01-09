f = open('S3cr37.png', 'wb', 1024000)
for line in open('/media/sf_j/Downloads/S3cr37.txt'):
#	print `line`
	f.write(line[:-1].decode('hex'))
