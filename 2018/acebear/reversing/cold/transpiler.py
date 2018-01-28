import sys
from StringIO import *
data = bytearray(open('vm.bin', 'rb').read()) # from binary
f = open('1.s', 'wb')
f.write('''
.intel_syntax noprefix
.global correct
.global gets
.global print
.global _main
.text
_main:
jmp main
correct:
ret
gets:
mov eax, [esp+4]
ret
print:
mov eax, [esp+4]
ret
main:
''')
def reg(x):
	if x > 3:
		return 'r%d' % x
	return ['eax', 'ebx', 'ecx', 'edx'][x & 3]
def extract(x):
	return sum(a << (i * 8) for i, a in enumerate(x))
locs = {}
def loc(x):
	data = 'loc_%x' % x
	locs[x] = data + ':\n'
	return data
cur = 0
raw = {
	0x8b: 0x8d
}
x = sys.stdout
lines = {}
def string(x):
	return str(data[x:]).split('\x00')[0]
code_end = 0x1d4
while cur < code_end:
	sys.stdout = x
	print '%05x:' % cur,
	op = data[cur]
	addr = cur
	cur += 1
	regs2 = (reg(data[cur] >> 4), reg(data[cur] & 3))
	regimm = (reg(data[cur] & 3), extract(data[cur+1:cur+5]))
	dword = extract(data[cur:cur+4])
	sys.stdout = StringIO()
	if op == 0:
		print 'call print'
	elif op == 16:
		print 'mov %s, 0x%x' % regimm
		cur += 5
	elif op == 17:
		print 'mov %s, %s' % regs2
		cur += 1
	elif op == 20:
		print 'mov %s, [%s]' % regs2
		cur += 1
	elif op == 21:
		print 'push %s' % reg(data[cur])
		cur += 1
	elif op == 32:
		print 'call print'
	elif op == 33:
		print 'call gets'
	elif op == 18:
		print 'movzx %s, byte ptr [%s]' % regs2
		cur += 1
	elif op == 173:
		print 'add %s, 0x%x' % regimm
		cur += 5
	elif op == 112:
		print 'cmp %s, %s' % regimm
		cur += 5
	elif op == 227:
		print 'jnz %s' % loc(dword)
		cur += 4
	elif op == 92:
		print 'sub %s, %s' % regs2
		cur += 1
	elif op == 91:
		print 'sub %s, %s' % regimm
		cur += 5
	elif op == 0x69:
		print 'cmp %s, [%s]' % regs2
		cur += 1
	elif op == 0x96:
		print 'call correct\nret'
	elif op == 232:
		print 'jnc %s' % loc(dword)
		cur += 4
	elif op == 174:
		print 'pop %s' % reg(data[cur])
		cur += 1
	elif op == 0xe2:
		print 'jz %s' % loc(dword)
		cur += 4
	elif op == 0xaa:
		print 'mov edi, 0x%x\ndiv edi' % dword
		cur += 4
	elif op == 169:
		print 'add %s, %s' % regs2
		cur += 1
	elif op == 0xf0:
		print 'xor %s, 0x%x' % regimm
		cur += 5
	elif op == 19:
		print 'mov [%s], %s' % regs2
		cur += 1
	elif op == 0xe0:
		print 'jmp %s' % loc(dword)
		cur += 4
	elif op == 0xef:
		print 'xor %s, [%s]' % regs2
		cur += 1
	elif cur - 1 in raw:
		print '.byte ' + ','.join('0x%x' % x for x in data[cur - 1:raw[cur - 1]])
		cur = raw[cur - 1]
	else:
		print 'implement %x' % op
	asm = sys.stdout.getvalue()
	sys.stdout = x
	print asm[:-1]
	lines[addr] = lines.get(addr, '') + asm
sys.stdout = x
for i in sorted(lines):
	f.write(locs.get(i, '') + lines[i])
f.write('.byte ' + ','.join('0x%x' % x for x in 'a' * (0x22f - 0x1c4) + data[cur:]))
print
# print string(0x22f)
# print string(0x2c1)
print 'Check 1.s for assembly'
exit()
