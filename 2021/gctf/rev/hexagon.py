from z3 import *
import struct

labels = {}
lines = list(x.strip() for x in open('disas.txt'))

for i, line in enumerate(lines):
	label = line[15:].strip().split(' ')[0]
	if ':' in label:
		labels[label[:-1]] = i

def tstbit(a, b):
	return a & (1 << b)

def add(a, b):
	return a + b

def not_(a):
	return (a ^ 0xffffffff)

def xor(a, b):
	return a ^ b

pc = labels['check_flag'] + 3
r2, r3 = BitVecs('r2 r3', 32)
flag = r2, r3
stack = []
for i in range(1000):
	op = lines[pc]
	if op.startswith('.text:0002037C'):
		break
	if '{' not in op:
		pc += 1
		continue
	if '}' not in op:
		x = pc
		while '}' not in lines[pc]:
			pc += 1
		pc += 1
		ops = [x[15:].replace('{','').replace('}','').strip() for x in lines[x:pc]]
		print(ops)
		if ops == ['r0 = r2', 'r2 = r0']:
			r0, r2 = r2, r0
			continue
		elif ops == ['r0 = r3', 'r3 = r0']:
			r0, r3 = r3, r0
			continue
		elif ops == ['r2 = r3', 'r3 = xor(r2, r0)']:
			r2, r3 = r3, r2 ^ r0
			continue
		elif 'tstbit' in op:
			nextpc = labels[ops[-1].split(' ')[-1]]
			exec(op.split('{')[1].strip().replace('#', ''))
			print(p0)
			if p0:
				print('Condition satisfied', '=' * 20)
				pc = nextpc
			continue
		else:
			exit()
	op = op.split('{')[1].split('}')[0].strip()
	print(op)
	op = op.replace('##', '')
	op = op.replace('#', '')
	op = op.replace('not', 'not_')
	if op.startswith('call'):
		stack.append(pc + 1)
		pc = labels[op.split(' ')[-1]]
		print('Calling', hex(pc), '=' * 20)
		continue
	if op == 'jumpr lr':
		pc = stack.pop()
		print('Returning', '=' * 20)
		continue
	if op.startswith('jump '):
		pc = labels[op.split(' ')[-1]]
		continue

	exec(op)
	pc += 1

s = Solver()
# r2, r3 = r3, r2
a, b = struct.unpack_from("<LL", b"\x97\xbf\x80m=\x0eE\x9dCongratulations! Flag is 'CTF{XXX}' where XXX is your input.\nTry again!\n", 0)
s.add(r2 == a, r3 == b)
print(s.check())
if s.check() == sat:
	print(b''.join([struct.pack("<L", x.as_long()) for x in [s.model()[flag[0]], s.model()[flag[1]]]]))