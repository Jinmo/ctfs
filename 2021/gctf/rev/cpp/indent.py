lines = []
indent = 0
for line in open('cpp.c', 'r'):
	line = line.lstrip()
	if line.startswith('#endif'):
		indent -= 1
	elif line.startswith('#else'):
		indent -= 1

	lines.append('    ' * indent + line)

	if line.startswith('#if'):
		indent += 1
	elif line.startswith('#else'):
		indent += 1

open('cpp.c', 'w').write(''.join(lines))