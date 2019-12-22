import sys

maps = {}

for line in open('fsmir2.sv'):
	if 'c <=' in line and "8'b" in line:
		x=line.split(': ')[0].strip()
		y=line.split('<=')[-1].strip(';\n ')
		maps[int(y[3:])] = int(x[3:], 2)
	if 'case(di)' in line:
		line = line.strip().split(' : ')[0]
		line = int(line[3:])
		if not line:
			continue
		sys.stdout.write(chr(maps[line]))
		maps={}
		# print line
