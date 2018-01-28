from z3 import *
from pwn import *
from ctypes import CDLL
import datetime

HOST, PORT = 'securelogin.acebear.site', 5001
# HOST, PORT = '0.0.0.0', 31338
sock = lambda: remote(HOST, PORT)
privkey = [BitVec('x[%d]' % i, 32) for i in range(16)]
def get_seed():
	return int(time.mktime(datetime.datetime.strptime(r.recvline().strip(), '%c').timetuple()))
s = Solver()
S = Solver()
value = 1
def parse(data):
	data = [data[i:i+4]for i in range(0, len(data), 4)]
	print data
	data = [int(x, 16) for x in data]
	print data
	return data
conds = []
privkeys = parse(open('../key', 'rb').read().strip())
libc = CDLL('libc.so.6')
while False:
	r = sock()
	r.recvuntil('time: ')
	t = get_seed()
	libc.srand(t)
	state = BitVecVal(0, 32)
	password = []
	for i in range(16):
		X = privkey[i]
		A = value
		R = libc.rand()
		R = R & 0xffff
		state = X * ((state ^ A ^ R) + 1) + (state ^ A ^ R)
		state = state & 0xffff
		password.append(state)
	r.send('a' * 32)
	print r.recvuntil('password:')
	r.send(('%04X' % value) * 16 + '\x00')
	value = random.getrandbits(16)
	r.recvuntil('Generated password: ')
	data = r.recvline().strip()
	print data
	data = parse(data)
	for x, y in zip(password, data):
		s.add(x == y)
		S.add(x == y)
		conds.append(x == y)
	for i in range(len(privkey)):
		s.add(privkey[i] & 0xffff == privkey[i])
		S.add(privkey[i] & 0xffff == privkey[i])
		conds.append(privkey[i] & 0xffff == privkey[i])
	if s.check() == unsat:
		s = Solver()
		conds = conds[:-32]
		for i in range(len(conds)):
			s.add(conds[i])
		print len(conds)
		r.close()
		continue
	else:
		print '!'
	l = [s.model()[x] for x in privkey]
	S.add(Or(*[y != x.as_long() for x, y in zip(l, privkey)]))
	r.close()
	if S.check() == sat:
		print 'continue..'
		continue
	else:
		break
else:
	for i in range(16):
		s.add(privkey[i] == privkeys[i])

rs = s.check()
target = parse('F05664E983F54E5FA6D5D4FFC5BF930743F60D8FC2C78AFBB0AF7C82664F2043')
if rs == sat:
	model = s.model()
	privkey = [model[privkey[i]] for i in range(16)]
	privkey = [x.as_long() for x in privkey]
	print map(hex, privkey)
	r = sock()
	r.recvuntil('time: ')
	t = get_seed()
	libc.srand(t)
	password = []
	input = [BitVec('x[%d]' % i, 32) for i in range(16)]
	state = BitVecVal(0, 32)
	for i in range(16):
		X = BitVecVal(privkey[i], 32)
		A = input[i]
		R = libc.rand()
		R &= 0xffff
		state = X * ((state ^ A ^ R) + 1) + (state ^ A ^ R)
		state = state & 0xffff
		password.append(state)
	s = Solver()
	for x, y in zip(target, password):
		s.add(x == y)
	for i in range(len(input)):
		s.add(input[i] & 0xffff == input[i])
	if s.check() == sat:
		for i in range(16):
			input[i] = s.model()[input[i]].as_long()
		input = ''.join('%04X' % x for x in input)
	else:
		print 'wtf'
		exit()
	r.send('a' * 32)
	r.send(input + '\x00')
	r.interactive()