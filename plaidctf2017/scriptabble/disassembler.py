from fasparser import *
from engine import *
import struct
i = 0
stack = []
tell = []
if True:
	path = 'example/apple.scpt'
f = load_file(path)
# pprint(f)
for code in f['data']:
	if code['kind'] == 'untypedPointerBlock':
		data = code['data'][2]['data']
		s = bytearray(data[-1])
		literals = data[-2]['data']
		break
# literals = literals[2]
off_16 = 'None'
semantic_mode = False
debug_mode = False
comments = {}
def word():
	global i
	r = struct.unpack(">H", s[i:i+2])[0]
	if r > 0x8000:
		r -= 0x10000
	i += 2
	return r
def push(x):
	global stack, semantic_mode, debug_mode
	if semantic_mode and debug_mode:
		print 'pushed', x,
	stack += [x]
	return x

def pop():
	return stack.pop()

def binary(_, a, b):
	a, b = b, a
	return '(' + str(a) + ' ' + _ + ' ' + str(b) + ')'

def unary(_, a):
	return _ + str(a)

def Undefined():
	return Object(2, 'undefined')

class Object:
	def __init__(self, typeIdx, value):
		self.typeIdx = typeIdx
		self.value = value

	def __str__(self):
		return '[Object %s]' % self.value

class Number(Object):
	def __init__(self, x):
		Object.__init__(self, 6, int(x))

	def __str__(self):
		if self.value > 16:
			return hex(self.value)
		else:
			return str(self.value)

class alias(Object):
	def __init__(self, idx, args):
		self.idx = idx
		self.args = args
		return
	def __str__(self):
		if self.idx == 4:
			return '(item %s of %s)' % (self.args[0], self.args[2])
		else:
			return 'T%d(%s)' % (self.idx, ', '.join(str(arg) for arg in self.args))

def variable(x):
	return '[Variable %d]' % x

def literal(x):
	if x >= len(literals):
		return '[L%d]' % x
	return literals[x]

tab = 0

while i < len(s):
	print " " * tab * 4, '%05x' % i,
	c = s[i]
	i += 1
	op = opcodes[c]
	if not semantic_mode:
		print op,
	if op == 'Jump':
		print 'jump', i + word(),
	elif op == 'PushLiteral':
		if semantic_mode:
			push(literal(c & 0xf)),
		else:
			print c & 0xf, '#', literal(c & 0xf),
	elif op == 'PushLiteralExtended':
		if semantic_mode:
			push(literal(word())),
		else:
			v = word()
			print v, '#', literal(v),
	elif op in ['Push0', 'Push1', 'Push2', 'Push3']:
		if semantic_mode:
			push(Number(op[4:])),
	elif op == 'PushIt':
		if semantic_mode:
			push(off_16),
	elif op == 'PushGlobal':
		if semantic_mode:
			v = literal(c & 0xf)
			push('gvar_%s' % v)
		else:
			v = literal(c & 0xf)
			print v,
	elif op == 'PushGlobalExtended':
		if semantic_mode:
			push('gvar_%d' % (word()))
		else:
			v = literal(word())
			print v,
	elif op == 'PopGlobal':
		if not semantic_mode:
			print literal(c & 0xf),
		else:
			print 'gvar_%s' % literal(c & 0xf)
	elif op == 'PopGlobalExtended':
		if not semantic_mode:
			print literal(word()),
		else:
			print 'gvar_%d' % literal(word())
	elif op == 'PopVariable':
		if not semantic_mode:
			print c & 0xf,
		else:
			print 'var_%d' % (c & 0xf)
	elif op == 'PopVariableExtended':
		print 'var_%d' % word()
	elif op == 'Tell':
		if semantic_mode:
			t = word()
			v = 'Tell%d' % t
			off_16 = v
		else:
			print word(),
			tab += 1
	elif op == 'Subtract':
		if semantic_mode:
			push(binary('-', pop(), pop())),
	elif op == 'Add':
		if semantic_mode:
			push(binary('+', pop(), pop())),
	elif op == 'Equal':
		if semantic_mode:
			push(binary('==', pop(), pop())),
	elif op == 'Concatenate':
		if semantic_mode:
			push(binary('&', pop(), pop())),
	elif op == 'Remainder':
		if semantic_mode:
			push(binary('%', pop(), pop())),
	elif op == 'Divide':
		if semantic_mode:
			push(binary('/', pop(), pop())),
	elif op == 'Multiply':
		if semantic_mode:
			push(binary('*', pop(), pop())),
	elif op == 'LessThanOrEqual':
		if semantic_mode:
			push(binary('<=', pop(), pop()))
	elif op == 'LessThan':
		if semantic_mode:
			push(binary('<', pop(), pop()))
	elif op == 'Power':
		if semantic_mode:
			push(binary('**', pop(), pop()))
	elif op == 'Negate':
		if semantic_mode:
			push(unary('-', pop()))
	elif op == 'PushUndefined':
		if semantic_mode:
			push(Undefined())
	elif op == 'PushVariable':
		if semantic_mode:
			push(variable(c & 0xf))
		else:
			print c & 0xf,
	elif op == 'PushVariableExtended':
		if semantic_mode:
			push(variable(word()))
		else:
			print word()
	elif op in ['MakeObjectAlias', 'MakeComp']:
		if not semantic_mode:
			t = c - 23
			print t, comments.get(t, '')
		else:
			t = c - 23
			idx = getSizeByIndex(t)
			v = alias(idx, [str(pop()) for _i in range(idx - 1)])
			push(v)
	elif op == 'SetData':
		if semantic_mode:
			push('GetData(' + ', '.join(map(str, [pop(), pop(), pop()])) + ')')
	elif op == 'GetData':
		if semantic_mode:
			push('GetData')
	elif op == 'Dup':
		if semantic_mode:
			v = pop()
			push(v)
			push(v)
	elif op == 'TestIf':
		if not semantic_mode:
			print hex(i + word()),
		else:
			v = i + word()
			print 'if',
			print pop(),
			print 'then goto',
			print hex(v),
	elif op == 'MessageSend':
		if semantic_mode:
			v = word()
			v = literal(v)
			r = '%r' % v
			push(r)
		else:
			v = word()
			print v, '#', literal(v),
	elif op == 'StoreResult':
		if semantic_mode:
			r = str(stack[-1])
			r += '()'
			print r
			push(r)
	elif op == 'PositionalMessageSend':
		if semantic_mode:
			v = word()
			v = literal(v)
			push('%s()' % v)
		else:
			v = word()
			print v, '#', literal(v),
	elif op == 'LinkRepeat':
		v = word() + i
		if semantic_mode:
			pass
		else:
			print hex(v)
	elif op == 'EndTell':
		if semantic_mode:
			pass
		else:
			tab -= 1
			pass
	elif op == 'RepeatInRange':
		if not semantic_mode:
			print word(),
		else:
			print word(),
	elif op == 'Return':
		if semantic_mode:
			print
	elif op == 'MakeVector':
		if semantic_mode:
			cnt = pop()
			push([pop() for _i in range(cnt)])
	else:
		if semantic_mode:
			print op
		else:
			print '<implement this>',
	print