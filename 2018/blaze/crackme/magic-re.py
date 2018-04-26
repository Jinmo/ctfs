from capstone import *
import struct

regs = 'ESP, EAX, ECX, EDX, EBX, WHAT, EBP, ESI, EDI'.split(', ')[::-1]
strings = ['AAAAaaaaCAAA q31EAAAFAAAGAAAHAAATu31', 'baaacaaadaaaeaaafaaagaaahaaa\x00\x00\x00baaaa', 'baaaaaaaCAAA q31EAAAFAAAGAAAHAAAXu31', 'caaadaaaeaaafaaagaaahaaa\x00\x00\x00baaacaaaC', 'baaacaaaCAAA q31EAAAFAAAGAAAHAAA\\u31', 'daaaeaaafaaagaaahaaa\x00\x00\x00aaaacaaaCAAA ', 'aaaacaaaCAAA q31EAAAFAAAGAAAHAAA\\u31', 'daaaeaaafaaagaaahaaa\x00\x00\x00aaaacaaaCAAA ', 'aaaabaaaCAAA q31EAAAFAAAGAAAHAAA\\u31', 'daaaeaaafaaagaaahaaa\x00\x00\x00aaaacaaaCAAA ', 'aaaabaaaDAAA q31EAAAFAAAGAAAHAAA\\u31', 'daaaeaaafaaagaaahaaa\x00\x00\x00aaaacaaaCAAA ', 'daaabaaaDAAA q31EAAAFAAAGAAAHAAA`u31', 'eaaafaaagaaahaaa\x00\x00\x00daaabaaaDAAA q31E', 'daaabaaaDAAA q31EAAAGAAAGAAAHAAA`u31', 'eaaafaaagaaahaaa\x00\x00\x00daaabaaaDAAA q31E', 'daaabaaaDAAA q31EAAAGAAAeaaaHAAAdu31', 'faaagaaahaaa\x00\x00\x00daaabaaaDAAA q31EAAAG', 'daaabaaaDAAA q31EAAAGAAAeaaaHAAA`u31', 'du31faaagaaahaaa\x00\x00\x00daaabaaaEAAA q31E', 'daaabaaaEAAA q31EAAAGAAAeaaaHAAA`u31', 'du31faaagaaahaaa\x00\x00\x00daaabaaaEAAA q31E', 'du31baaaEAAA q31EAAAGAAAeaaaHAAAdu31', 'faaagaaahaaa\x00\x00\x00daaabaaaDAAA q31EAAAG', 'du31baaaEAAA q31EAAAGAAAdaaaHAAAdu31', 'faaagaaahaaa\x00\x00\x00daaabaaaDAAA q31EAAAG', 'du31aaaaEAAA q31EAAAGAAAdaaaHAAAdu31', 'faaagaaahaaa\x00\x00\x00daaabaaaDAAA q31EAAAG', 'du31aaaaEAAA q31EAAAGAAAdaaaHAAA`u31', 'EAAAfaaagaaahaaa\x00\x00\x00du31aaaaEAAA q31E', 'du31aaaaEAAA q31EAAAGAAAdaaaHAAA\\u31', '`u31EAAAfaaagaaahaaa\x00\x00\x00du31aaaaEAAA ', 'du31aaaaEAAA q31EAAAGAAAdaaaHAAAXu31', 'GAAA`u31EAAAfaaagaaahaaa\x00\x00\x00du31aaaaE', 'du31aaaaEAAA q31EAAAGAAAdaaaHAAATu31', 'EAAAGAAA`u31EAAAfaaagaaahaaa\x00\x00\x00du31a', 'du31aaaaEAAA q31FAAAGAAAdaaaHAAATu31', 'EAAAGAAA`u31EAAAfaaagaaahaaa\x00\x00\x00du31a', 'du31aaaaEAAA q31FAAAGAAAdaaaHAAAPu31', 'Tu31EAAAGAAA`u31EAAAfaaagaaahaaa\x00\x00\x00\x00', 'du31aaaaEAAA q31FAAAGAAAcaaaHAAAPu31', 'Tu31EAAAGAAA`u31EAAAfaaagaaahaaa\x00\x00\x00\x00', 'cu31aaaaEAAA q31FAAAGAAAcaaaHAAAPu31', 'Tu31EAAAGAAA`u31EAAAfaaagaaahaaa\x00\x00\x00\x00', 'cu31`aaaEAAA q31FAAAGAAAcaaaHAAAPu31', 'Tu31EAAAGAAA`u31EAAAfaaagaaahaaa\x00\x00\x00\x00', 'Tu31`aaaEAAA q31FAAAGAAAcaaaHAAATu31', 'EAAAGAAA`u31EAAAfaaagaaahaaa\x00\x00\x00du31a', 'Tu31aaaaEAAA q31FAAAGAAAcaaaHAAATu31', 'EAAAGAAA`u31EAAAfaaagaaahaaa\x00\x00\x00du31a', 'Tu31aaaaEAAA q31FAAAGAAAcaaaHAAASu31', '1EAAAGAAA`u31EAAAfaaagaaahaaa\x00\x00Tu31a', 'Tu31aaaaEAAA q31FAAAGAAAdaaaHAAASu31', '1EAAAGAAA`u31EAAAfaaagaaahaaa\x00\x00Tu31a', 'Uu31aaaaEAAA q31FAAAGAAAdaaaHAAASu31', '1EAAAGAAA`u31EAAAfaaagaaahaaa\x00\x00Tu31a', '1EAAaaaaEAAA q31FAAAGAAAdaaaHAAAWu31', 'AGAAA`u31EAAAfaaagaaahaaa\x00\x001EAAaaaaE', '1EAAaaaaEAAA q31FAAAGAAAcaaaHAAAWu31', 'AGAAA`u31EAAAfaaagaaahaaa\x00\x001EAAaaaaE', '1EAAaaaaEAAA q31FAAAAGAAcaaaHAAA[u31', 'A`u31EAAAfaaagaaahaaa\x00\x00A`u3aaaaEAAA ', 'A`u3aaaaEAAA q31FAAAAGAAcaaaHAAA_u31', '1EAAAfaaagaaahaaa\x00\x00A`u3aaaaEAAA q31G', 'A`u3aaaaEAAA q31GAAAAGAAcaaaHAAA_u31', '1EAAAfaaagaaahaaa\x00\x00A`u3aaaaEAAA q31G', 'A`u3aaaaEAAA q31GAAAAGAAcaaaHAAA^u31', '31EAAAfaaagaaahaaa\x00A`u3aaaaEAAA q31G', 'A`u3aaaaEAAA q31GAAAAGAAdaaaHAAA^u31', '31EAAAfaaagaaahaaa\x00A`u3aaaaEAAA q31G', 'A`u3aaaaEAAA q31GAAAAGAAdaaaHAAAZu31', 'GAAA31EAAAfaaagaaahaaa\x00A`u3aaaaEAAA ', 'A`u3aaaaEAAA q31GAAAAGAAdaaaHAAAVu31', 'GAAAGAAA31EAAAfaaagaaahaaa\x00A`u3aaaaE', 'A`u3aaaaEAAA q31GAAAAGAAGAAAHAAAZu31', 'GAAA31EAAAfaaagaaahaaa\x00A`u3aaaaEAAA ', 'GAAAaaaaEAAA q31GAAAAGAAGAAAHAAA^u31', '31EAAAfaaagaaahaaa\x00A`u3aaaaEAAA q31G', 'GAAAaaaaEAAA q31GAAAAGAAHAAAHAAA^u31', '31EAAAfaaagaaahaaa\x00A`u3aaaaEAAA q31G', 'GAAA`aaaEAAA q31GAAAAGAAHAAAHAAA^u31', '31EAAAfaaagaaahaaa\x00A`u3aaaaEAAA q31G', 'GAAA`aaaEAAA q31GAAAAGAAHAAAHAAA_u31', '1EAAAfaaagaaahaaa\x00\x00A`u3aaaaEAAA q31G', '1EAA`aaaEAAA q31GAAAAGAAHAAAHAAAcu31', 'Afaaagaaahaaa\x00\x001EAAaaaaEAAA q31GAAAA', '1EAAaaaaEAAA q31GAAAAGAAHAAAHAAAcu31', 'Afaaagaaahaaa\x00\x001EAAaaaaEAAA q31GAAAA', '1EAAaaaaEAAA q31GAAAAGAAHAAAHAAA_u31', 'EAAAAfaaagaaahaaa\x00\x001EAA`aaaEAAA q31G', '1EAA`aaaEAAA q31GAAAAGAAHAAAHAAA_u31', 'EAAAAfaaagaaahaaa\x00\x001EAA`aaaEAAA q31G', 'EAAA`aaaEAAA q31GAAAAGAAHAAAHAAAcu31', 'Afaaagaaahaaa\x00\x001EAAaaaaEAAA q31GAAAA', 'EAAA`aaaEAAA q31GAAABGAAHAAAHAAAcu31', 'Afaaagaaahaaa\x00\x001EAAaaaaEAAA q31GAAAA', 'EAAA`aaaAfaa q31GAAABGAAHAAAHAAAgu31', 'agaaahaaa\x00%255s\x00A problem with mmap ']
def to_regs(x):
	x = struct.unpack("<9L", x)
	y = {}
	for reg, value in zip(regs, x):
		y[reg] = value
	return y

# This prints all possible options
cs = Cs(CS_ARCH_X86, CS_MODE_32)
for i in range(64, 96):
	dis = cs.disasm(chr(i) * 100, 0x3133700c).next()
	print dis.mnemonic + ' ' + dis.op_str, '/',

print 'end'

# ... and constructed a simulator and code-generator with it. there is some multiple candidates because multiple candidates can be found on push <reg>
def diff(x, y, prevStack, stack):
	X = x
	Y = y
	diffs = {}
	for a in y:
		if y[a] != x[a]:
			# print a, '%08x'%x[a], '->', '%08x'%y[a]
			diffs[a] = x[a], y[a]
	if len(diffs.keys()) == 1 and diffs.keys()[0] in regs:
		x, y = diffs.values()[0]
		if abs(x-y) == 1:
			print {-1: 'dec', 1: 'inc'}[y - x] + ' ' + diffs.keys()[0]
		elif abs(x-y) == 4:
			if x > y:
				print 'PUSH',
				#print `prevStack`
				#print `stack`
				found = 0
				for a, b in X.items():
					if b == struct.unpack("<L", stack[:4])[0]:
						print a,
						found = 1
						# break
				if found == 0:
					print '?'
				print
			else:
				print 'POP EAX'
		else:
			print 'wtf'
			exit()
	elif 'ESP' in diffs:
		assert x['ESP'] + 4 == y['ESP']
		print 'pop', filter(lambda x: x != 'ESP', diffs.keys())
	else:
		print 'INC EAX'

prev = initial = to_regs("AAAABAAACAAADAAAEAAAFAAAGAAAHAAAPu31")
base = initial['ESP']
print '%x' % initial['ESP']
prevStack = "aaaabaaacaaadaaaeaaafaaagaaahaaa"
for i in range(0, len(strings), 2):
	cur = to_regs(strings[i])
	stack = strings[i+1]
	diff(prev, cur, prevStack, stack)
	prev = cur
	prevStack = stack
	# print '-' * 80