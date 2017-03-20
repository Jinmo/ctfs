import struct
from z3 import *
from engine import *

vm = [opcodes[index*5:index*5+5] for index in indexes]
cache = {}

def save(o, data):
	cache[o] = data

def mem(addr):
	if addr not in cache:
		cache[addr] = BitVec('mem[%x]' % addr, 1)
		print 'Caching %x...' % addr
	return cache[addr]

input = [Bool('input[%d_%d]' % (i >> 3, i % 8)) for i in range(len(inputIndexes))]
cache[0] = BoolVal(False)
cache[1] = BoolVal(True)

for i in range(len(inputIndexes)):
	cache[inputIndexes[i]] = input[i]

def _or(o, a, b):
#	print '%x = %x | %x' % (o, a, b)
	save(o, Or(mem(a), mem(b)))
	return

def _xor(o, a, b):
#	print '%x = %x ^ %x' % (o, a, b)
	save(o, Xor(mem(a), mem(b)))
	return

def _multiplex(o, c, a, b):
#	print '%x = %x ? %x : %x' % (o, c, a, b)
	save(o, If(mem(c), mem(a), mem(b)))
	return

def _and(o, a, b):
#	print '%x = %x & %x' % (o, a, b)
	save(o, And(mem(a), mem(b)))
	return

for opcode in vm:
	op, src1, src2, src3, output = opcode
	if op == 2:
		_or(output, src1, src2)
	if op == 3:
		_xor(output, src1, src2)
	if op == 4:
		# if !src1, src2
		# if src1, src3
		_multiplex(output, src1, src2, src3)
	if op == 1:
		_and(output, src1, src2)

s = Solver()
result = []

for index in outputIndexes:
	print hex(index),
	result.append(mem(index))

print
# print simplify(result[0])

non_string = 'C'
start = 0
for i in range(len(non_string) * 8):
	c = ((ord(non_string[i >> 3]) >> (i % 8)) & 1 == 1)
	print c
	expr = result[i+start*8] == c
	s.add(expr)

result = s.check()
if result == sat:
	model = s.model()
	input = [int(eval(str(model[input[i]]))) for i in range(len(input))]
	print input
	input = [reduce(lambda x, y: x | (y[0] << y[1]), zip(input[i:i+8], range(8)), 0) for i in range(0, len(input), 8)]
	print bytearray(input)
else:
	print result