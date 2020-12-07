.intel_syntax noprefix
.globl r64
.globl w64

r64:
push r11
push r12
push r13
mov r11, 0x7331733173317331
mov r13, rdi
.ascii "\xd4"
mov rax, r12
pop r13
pop r12
pop r11
ret

w64:
push r11
push r12
push r13
mov r11, 0x1337133713371337
mov r12, rsi
mov r13, rdi
.ascii "\xd4"
pop r13
pop r12
pop r11
ret
