import struct
mem=bytearray(open('vm2.bin','rb').read())
pc=0x2000
i=0

def byte():
	global pc
	pc += 1
	return mem[pc-1]

def reg(x):
	return 'r%d'%x

def imm(x):
	return '0x%x'%x

xorkey = (0, 0)

while i < 0x100 and pc < 0x2108:
	i += 1
	print '0x%05x:' % pc,
	op = byte() ^ xorkey[0]
	b1=byte() ^ xorkey[1]
	b2=byte() ^ xorkey[0]
	b3=byte() ^ xorkey[1]
	word=b2+b3*256
	if op == 0:
		print 'raise'
	elif op == 1:
		print 'li %s, %s' % (reg(b1), imm(word))
	elif op == 3:
		print 'add %s, %s, %s' % (reg(b1), reg(b2), reg(b3))
	elif op == 8:
		print 'str [%s], %s' % (reg(b1), reg(b2))
	elif op == 7:
		print 'ldr %s, [%s]' % (reg(b1), reg(b2))
	elif op == 4:
		print 'xor %s, %s, %s' % (reg(b1), reg(b2), reg(b3))
	elif op == 6:
		print 'bl %s, %s, %s' % (reg(b1), reg(b2), reg(b3))
	elif op == 12:
		print 'call write(%s, %s)' % (reg(b1), reg(b2))
	elif op == 13:
		print 'call exit(%s)' % imm(word)
	elif op == 14:
		print '# xorkey = 0x%08x' % (word | word << 16)
		xorkey = (word & 0xff, word >> 8)
	elif op == 11:
		print 'r0 = call read(%s, %s)' % (reg(b1), reg(b2))
	elif op == 15:
		print 'beq %s, %s, 0x2000+%s' % (reg(b1), reg(b2), reg(b3))
	else:
		print op
		exit()