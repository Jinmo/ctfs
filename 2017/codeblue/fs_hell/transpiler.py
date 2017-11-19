from z3 import *
import re

class Registers(object):
	def __init__(self, x):
		self.storage = [0] * x

	def __setitem__(self, x, y):
		self.storage[x] = y & 0xffff

	def __getitem__(self, x):
		return self.storage[x] & 0xffff

class vm:
	regs = Registers(24)
	pass
input_fp = [ZeroExt(7, BitVec('input[%d]' % i, 8)) for i in range(65536)]
class Reg:
	def __init__(self, index):
		self.index = index
		pass
	def assign(self, x):
		vm.regs[self.index] = x
class Assign:
	def __init__(self, x):
		self.x = x
		pass
	def assign(self, x):
		input_fp[self.x] = x

trueval = BitVecVal(1, 16)
falseval = BitVecVal(0, 16)

for i, line in enumerate(open('program.txt', 'r')):
	line = line.strip()
	jump = False
	if 0:
		args = [
		      vm.regs[8],
		      vm.regs[12],
		      vm.regs[16],
		      vm.regs[20],
		      input_fp[vm.regs[20]],
		      Reg(8),
		      Reg(12),
		      Reg(16),
		      Reg(20),
		      Assign(vm.regs[20]), # 10
		      If(vm.regs[8] == 0, trueval, falseval),
		      (vm.regs[8] & 0x8000) != 0,
		      Reg(4),
		      0
		]
	else:
		args = [
			'r8',
			'r12',
			'r16',
			'r20',
			'mem[r20]',
			'&r8=',
			'&r12=',
			'&r16=',
			'&r20=',
			'(mem + r20)=',
			'r8 == 0',
			'((signed short)r8) < 0',
			'r4=',
			'0'
		]
	exts = line.split('%')[1:]
	r = 0
	x = ''
	print 'L%d:' % i,
	if not line:
		print
		continue
	for cmd in exts:
		op = cmd[-1]
		arg = re.match(r'^[0-9]+', cmd).group(0)
		arg = int(arg) - 1
		if op == 'n':
			if cmd.endswith('hhn'):
				# r &= 0xff
				mask = 0xff
			elif cmd.endswith('hn'):
				# r &= 0xffff
				mask = 0xffff
				pass
			else:
				print '?'
				exit()
			# args[arg].assign(r)
			if args[arg] == 'r4=':
				jump = True
			if mask == 0xff:
				prefix = '*(unsigned char *)%s (unsigned char)' % (args[arg], )
			else:
				prefix = '*(unsigned short *)' + args[arg]
		elif op == 'd':
			assert arg == 13
			if '.*' in cmd:
				z = int(re.match(r'^[0-9]+', cmd.split('.*')[1]).group(0)) - 1
				# r += args[z]
				x += ' + %s' % (args[z])
			else:
				d = int(re.match(r'^[0-9]+', cmd.split('.')[1]).group(0))
				# r += d
				if d & 0x8000:
					d -= 0x10000
				if d >= 0:
					x += ' + %d' % (d, )
				else:
					x += ' - %d' % (-d, )
		else:
			print 'wtf?', cmd, `op`
			exit()
	if not jump:
		print prefix, '(', x.lstrip(' + '), ');'
	else:
		if '<' in x or '=' in x:
			print 'if(', x, ') goto L%d;' % (i + 2)
		else:
			print 'goto L%d;' % (i + int(x) + 1)
# solve(vm.regs[8] == 0)
exit()

