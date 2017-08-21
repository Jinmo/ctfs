
.globl main
.globl buf
main:
bl initz
ldr r3, =0xc0ffee
ldr r9, =#100000
mov r8, #0
mov r0, r3
ldr r1, =#0x100f8+1
ldr r1, =#0x10290+1
blx r1
loop:
ldr r1, =#0x10200+1
blx r1
push {r0}
mov r0, #1
mov r1, sp
mov r2, #4
mov r7, #4
svc #0
pop {r0}
sub r9, #1
bne loop
format:
.asciz "%p\n"
buf:
.incbin "main.bin"
buf_end:
.code 16
.globl getchar_
.globl getchar__end
getchar_:
push {r1-r7}
mov r0, #0
push {r0}
mov r0 ,#0
mov r1, sp
mov r2, #1
mov r7, #3
svc #0
pop {r0}
pop {r1-r7}
bx lr
getchar__end:

.globl putchar_
.globl putchar__end
putchar_:
push {r0-r7}
push {r0}
mov r0 ,#1
mov r1, sp
mov r2, #1
mov r7, #4
svc #0
pop {r0}
pop {r0-r7}
bx lr
putchar__end:
