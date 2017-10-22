from z3 import *
import re
import struct

data = open('C:/Users/berry/Downloads/nobs_a6ad4001a8a7ba83c0c1c448bae441b321dadfd93b2cdb0fa9a365db7c09c4a4', 'rb').read()
space = re.compile(r'[\t ]+')
pack = lambda *args: bytearray(struct.pack(*args)) if hasattr(args[1], '__trunc__') else slowpack(*args)

def slowpack(format, text):
	size = {'Q': 8, 'L': 4, 'H': 2}[format[1]]
	r = []
	for i in range(size):
		r.append(ZeroExt(56, Extract(7 + i * 8, i * 8, text)))
	return r

insn = {}
nexts = {}
prev = None
for line in open('disas.txt'):
	line = space.sub(line, ' ')
	line = line.strip()
	line = line.split('\t')
	if len(line) < 3:
		continue
	addr = line[0].strip(':')
	addr = int(addr, 16)
	if len(line) == 4:
		line[3] = line[3].split(',')
	insn[addr] = line[2:]
	if prev is not None:
		nexts[prev] = addr
	prev = addr

STACK = 0x100000
regs = {'pc': 0x10400, 'sp': STACK, 'a0': 2, 'a1': STACK, 'ra': 0xffffffff}
mem = {}
for i in range(12):
	regs['s%d' % i] = 0
count = 0

MAX = 100000

imm = lambda x, base=16: int(x, base) if x.startswith('0x') else int(x.split(' ')[0])
ind = lambda x: imm(x.split('(')[0]) + regs[x.split('(')[1].split(')')[0]]
jmptarget = lambda x: int(x.split(' ')[0], 16)

def load(addr, size):
	r = 0
	for i in range(size):
		r |= mem[addr+i] << (i * 8)
	return r

def store(addr, value):
	for i in range(len(value)):
		mem[addr+i] = value[i]

ARG = STACK + 100
mask32 = 0xffffffff
mask64 = 2 ** 64 - 1
store(ARG, [ZeroExt(56, BitVec('input[%d]' % i, 8)) for i in range(50)])
store(regs['a1'] + 8, pack("<Q", ARG))
store(0x10000, bytearray(data))

avoid = [0x1902e]

solver = Solver()

def jump(cond, target):
	global nextpc, avoid
	if type(cond) == bool:
		nextpc = nextpc if cond == False else target
	else:
		if nextpc in avoid:
			solver.add(cond)
		elif target in avoid:
			solver.add(Not(cond))
		else:
			solver.add(cond)
		if solver.check() == sat:
			print solver.model()
			exit()
			nextpc = target
		else:
			print 'unsolvable'

while count < MAX:
	pc = regs['pc']
	if pc not in insn:
		print 'wtf'
		exit()
	nextpc = nexts[pc]
	cur = insn[pc]
	op = cur[0]
	x = cur[1]
	print hex(pc), cur
	if op == 'addi':
		regs[x[0]] = regs[x[1]] + imm(x[2])
	elif op == 'sd':
		addr = ind(x[1])
		value = pack("<Q", regs[x[0]] & mask64)
		store(addr, value)
	elif op == 'li':
		value = imm(x[1])
		regs[x[0]] = value
	elif op == 'beq':
		cond = regs[x[0]] == regs[x[1]]
		jump(cond, jmptarget(x[2]))
	elif op == 'ld':
		regs[x[0]] = load(ind(x[1]), 8)
	elif op == 'lui':
		regs[x[0]] = imm(x[1]) << 12
	elif op == 'lhu':
		regs[x[0]] = load(ind(x[1]), 2)
	elif op == 'xor':
		regs[x[0]] = regs[x[1]] ^ regs[x[2]]
	elif op == 'slli':
		regs[x[0]] = (regs[x[1]] << imm(x[2])) & mask64
	elif op == 'srli':
		regs[x[0]] = (regs[x[1]] >> imm(x[2])) & mask64
	elif op == 'mulw':
		regs[x[0]] = regs[x[1]] * regs[x[2]] & mask32
	elif op == 'addiw':
		regs[x[0]] = regs[x[1]] + imm(x[2]) & mask32
	elif op == 'addw':
		regs[x[0]] = regs[x[1]] + regs[x[2]] & mask32
	elif op == 'mv':
		regs[x[0]] = regs[x[1]]
	elif op == 'sw':
		store(ind(x[1]), pack("<L", regs[x[0]] & mask32))
	elif op == 'xori':
		regs[x[0]] = regs[x[1]] ^ imm(x[2])
	elif op == 'lw':
		regs[x[0]] = load(ind(x[1]), 4)
	elif op == 'sh':
		store(ind(x[1]), pack("<H", regs[x[0]] & 0xffff))
	elif op == 'add':
		regs[x[0]] = regs[x[1]] + regs[x[2]] & mask64
	elif op == 'slliw':
		regs[x[0]] = (regs[x[1]] << imm(x[2])) & mask32
	elif op == 'lbu':
		regs[x[0]] = load(ind(x[1]), 1)
	elif op == 'or':
		regs[x[0]] = regs[x[1]] | regs[x[2]]
	elif op == 'bne':
		cond = regs[x[0]] != regs[x[1]]
		jump(cond, jmptarget(x[2]))
	elif op == 'beqz':
		cond = regs[x[0]] == 0
		jump(cond, jmptarget(x[1]))
	else:
		print 'implement', op
		exit()
	regs['pc'] = nextpc
	count += 1