chunks = {}
max_addr=-1
for line in open('log'):
	line=line.strip()
	if line.startswith('malloc'):
		addr=int(line.split(' = ')[-1],16)
		size=int(line.split('(')[1].split(')')[0],16)
		if addr>max_addr:
			max_addr=addr
		print(line, hex(addr-max_addr))
		chunks[addr]=size
	elif line.startswith('free'):
		addr=int(line.split('(')[1].split(')')[0],16)
		chunks[addr] = -size
	else:
		print(line)

chunks = sorted(chunks.items(), key=lambda x: x[0])
expected_next=0
for addr, size in chunks:
	if size < 0:
		continue
	if expected_next and expected_next<addr:
		print(f"[freed 0x{expected_next:x} size:0x{addr-expected_next:x}]")
	print(hex(addr), hex(size))
	_size=max(size,0xc)+0xf&~0xf
	expected_next=addr+_size