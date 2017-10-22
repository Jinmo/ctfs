import os

os.system('G0AL > output.txt')

r = list(open('output.txt', 'rb'))
print 'Executed powershell script:'
print r[1].decode('base64').decode('utf16')

print 'Before then.. this is executed:'
print r[0]
print 'Be sure to adjust this variable.'

print 'It executes shellcode: (base64 encoded)'
print r[2]

code = r[2].decode('base64')
print 'This shellcode is saved in output.bin'
open('output.bin', 'wb').write(code)

print 'You\'ll notice that some first characters in powershell script (first one) is corrupted'
print 'If you deleted that part, you can just execute the shellcode and see the flag'
print 'Now let\'s disassemble code'

from capstone import *

flag = ''
codes = Cs(CS_ARCH_X86, CS_MODE_32)
for op in codes.disasm(code, 0):
	if op.mnemonic == 'push' and op.size == 5:
		flag = op.bytes[1:] + flag
	print op.mnemonic + ' ' + op.op_str

print
print 'flag here!'
print `flag`