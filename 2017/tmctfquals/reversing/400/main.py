from ctypes import *

import ctypes
import struct
import os
import sys

############################################################
# Part 1. Library part. For routines you can jump to part 2
############################################################

import hooklib
from hooklib import Process

############################################################
# Part 2. Hooking & IPC part
############################################################

# Find the window
for i in range(1000):
    wp = ctypes.windll.user32.FindWindowA(
        0, 'TMCTF2017 - ScreenKeypad - OEP: 0x00403AE0 - %d/41216' %
        i)
    if wp:
        break

# .. and pid for it
pid = c_long(0)
ctypes.windll.user32.GetWindowThreadProcessId(wp, byref(pid))

# Open the process
if pid == 0:
    print 'OpenProces failed! First run screen keypad'
    exit()

p = Process.attach(pid)

# a pipe pair with destination process for IPC
pipein, pipeout = c_long(0), c_long(0)
windll.kernel32.CreatePipe(byref(pipein), byref(pipeout), None, 1)

# Duplicated file handle will be here
tp = c_long(0)

# Let's do it!
cp = windll.kernel32.GetCurrentProcess()
windll.kernel32.DuplicateHandle(
    c_void_p(cp), pipeout, p, byref(tp), 0, False, 2)

# Now hook some APIs. First, enumerate modules
# Create a <module name: base address> map
m = p.modules()

# Will suspend all threads and resume it in end
ts = p.threads()

# IPC helper function
trampoline = hooklib.va(p, c_void_p(0), c_void_p(0x1000), 0x3000, 0x40)
print windll.kernel32.GetLastError()
c = hooklib.asm('''
    sub rsp, 8
    mov rcx, %d
    movabs rax, %d
    mov r9, rsp
    sub rsp, 40
    mov qword ptr [rsp+32], 0
    call rax
    add rsp, 40
    add rsp, 8
    ret
    ''' % (tp.value, hooklib.addr(c_void_p(m['kernel32.dll']), 'WriteFile')))

z = c_long(0)
hooklib.wpr(p, trampoline, c, len(c), byref(z))


ts = [
    windll.kernel32.OpenThread(
        hooklib.THREAD_ALL_ACCESS,
        False,
        t) for t in ts]

for t in ts:
    windll.kernel32.SuspendThread(t)


class RECT(Structure):
    _fields_ = [
        ('left', c_int32),
        ('top', c_int32),
        ('right', c_int32),
        ('bottom', c_int32)]

r = RECT()
windll.user32.GetWindowRect(wp, r)

hook = p.hook

hook('user32.dll', 'SetCursorPos', '''
    push 0
    push rdx
    push rcx
    push 1
    mov rdx, rsp
    mov r8, 32
    mov rax, %d
    call rax
    add rsp, 32
    ret
    z:
    ''' % trampoline)

hook('user32.dll', 'SetWindowPos', '''
    ret
    cmp r8, 8
    jnz return
    push rcx
    push rdx
    push r8
    push r9
    sub rsp, 40
    lea rdx, [rip+z]
    mov qword ptr [rdx], 0
    mov r8, 255
    movabs rax, %d
    call rax
    add rsp, 40
    pop r9
    pop r8
    pop rdx
    pop rcx
    lea rax, [rip+z]
    push [rax]
    push r9
    push r8
    push 2
    mov rdx, rsp
    mov r8, 32
    mov rax, %d
    call rax
    add rsp, 32
    return:
    ret
    z:
    ''' % (
    hooklib.addr(c_void_p(m['user32.dll']), 'GetWindowTextA'),
    trampoline)
)

hook('kernel32.dll', 'GetTickCount', '''
    rdtsc
    ret
    ''')

hook('kernel32.dll', 'Beep', 'ret')

for t in ts:
    windll.kernel32.ResumeThread(t)

file = open('output.bin', 'wb')


def write(x):
    global offset
    # sys.stdout.write(x)
    if offset % 100 == 0:
        print '\r%d/41216' % (offset),
    file.write(x)
    file.flush()

x = c_long(0)
buf = c_buffer('\x00' * 100)
_map = map
map = []

# Button X offsets from mspaint
Xs = [
    8,
    39,
    71,
    102,
    133,
    164,
    195,
    226,
    257,
    288,
    319,
    350,
    381,
    412,
    443,
    474,
    474 +
    31]
offset = 0
delta = -1
write('3')
offset += 1
for i in range(41216):
    x.value = 0
    if windll.kernel32.ReadFile(
            c_void_p(pipein.value), buf, c_void_p(32), byref(x), c_void_p(0)) == 0:
        print 'read..wtf'
        exit()
    type, X, Y, Z = struct.unpack("<4Q", buf.raw[:32])
    if type == 1:
        _X, _Y = X, Y
        X -= r.left + 10
        Y -= r.top + 40
        f = 0
        z = 15
        for A in Xs[::-1]:
            if A + 27 >= X >= A - 3:
                # print X - A
                break
            z -= 1
        Z = z % 16
        Z = '%x' % Z
        write(Z)
        # sys.stdout.write(' ' * 8 + '%d %d %d %s\n' % (z, X, Y, Z))
        delta -= 1
        offset += 1
    elif type == 2:
        if X == 8:
            map.append(chr(Z))
            print map
    else:
        print 'wtf'
        exit()

print 'done'
file.close()
