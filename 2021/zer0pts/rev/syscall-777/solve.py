from z3 import *
import struct
args = [BitVec('x%d' % i, 32) for i in range(14)]
def process(args):
	mem = [None] * 100
	mem[0] = args[0] # 0018
	mem[1] = args[1] ^ mem[0]
	mem[2] = args[2] ^ mem[1]
	mem[3] = args[3] ^ mem[2]
	mem[4] = mem[0] + mem[1] + mem[2] + mem[3] # 0038
	mem[5] = mem[0] - mem[1] + mem[2] - mem[3] # 0046
	mem[6] = mem[0] + mem[1] - mem[2] - mem[3] # 0054
	mem[7] = mem[0] - mem[1] - mem[2] + mem[3]
	mem[8] = mem[4] | mem[5] # 0066
	mem[8] = (mem[6] & mem[7]) ^ mem[8] # 0072
	mem[9] = mem[5] | mem[6] # 0076
	mem[9] = (mem[7] & mem[4]) ^ mem[9]
	mem[10] = mem[6] | mem[7] # 0086
	A = mem[4] & mem[5]
	A ^= mem[10]
	mem[10] = A # 0092
	A = mem[7] | mem[4]
	mem[11] = A # 0096
	A = mem[5] & mem[6]
	A ^= mem[11]
	mem[11] = A # 0102
	return mem

values = [
[4255576062, 3116543486, 3151668710, 4290701286], # zer0pts{????????
[4139379682, 3602496994, 3606265306, 4143147994], # pts{????????????
[2307981054, 3415533530, 3281895882, 2174343406],
[1933881070, 2002783966, 1601724370, 1532821474],
[3098492862, 3064954302, 3086875838, 3120414398],
[1670347938, 4056898606, 2583645294, 197094626],
[4192373742, 4088827598, 3015552726, 3119098870],
[4025255646, 2813168974, 614968622, 1827055294],
[3747612986, 1340672294, 1301225350, 3708166042],

[4127179254, 4126139894, 665780030, 666819390],
[2673307092, 251771212, 251771212, 2673307092],

[2720551936, 1627051272, 1627379644, 2720880308], # ????????????zer0
[530288564, 530288564, 3917315412, 3917315412],   # ????????zer0pts{
[2130820044, 2115580844, 2130523044, 2145762244], # ????zer0pts{????
]
s = Solver()
for x in args:
	for i in range(4):
		v = Extract(i * 8 + 7, i * 8, x)
		s.add(v & 0x80 == 0)

values = values
s.add(args[0] == struct.unpack("<L", b'zer0')[0])
s.add(args[1] == struct.unpack("<L", b'pts{')[0])

for j in range(len(values)):
	if j >= 10 and j < len(values) - 3:
		continue
	print(j)
	mem = process((args[j], args[(j + 1) % 14], args[(j + 2) % 14], args[(j + 3) % 14]))
	# if j == 9:
	# 	j = 10
	for i in range(4):
		cond = mem[8 + i] == values[j][i]
		s.add(cond)

if (s.check()) == sat:
	print('yey')
	flag=b''
	while True:
		for x in args:
			l = s.model()[x].as_long()
			if l == 0:
				continue
			flag+=struct.pack("<L", l)
			print(x, flag)

		cond = []
		for x in args:
			val = s.model()[x]
			if val is not None:
				cond.append(x != val)
		s.add(Or(*cond))
		s.check()
		break
