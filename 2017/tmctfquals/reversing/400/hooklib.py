from keystone import *
from ctypes import *

import ctypes
import struct

PROCESS_ALL_ACCESS = 2035711
THREAD_ALL_ACCESS = 0x001F03FF

# Shortcuts for most used APIs
wpr = ctypes.windll.kernel32.WriteProcessMemory
addr = ctypes.windll.kernel32.GetProcAddress
va = ctypes.windll.kernel32.VirtualAllocEx
vp = ctypes.windll.kernel32.VirtualProtectEx
addr.restype = va.restype = c_void_p

# For enumerating modules

DWORD = c_long
LONG = c_longlong


class THREADENTRY32(Structure):
    _fields_ = [
        ('dwSize', DWORD),
        ('cntUsage', DWORD),
        ('th32ThreadID', DWORD),
        ('th32OwnerProcessID', DWORD),
        ('tpBasePri', LONG),
        ('tpDeltaPri', LONG),
        ('dwFlags', DWORD)
    ]

ks = Ks(KS_ARCH_X86, KS_MODE_64)


def asm(x):
    'Assembler'
    return str(bytearray(ks.asm(x)[0]))

def _addr_to_module(p, x):
    buf = (c_char * 1000)()
    x = c_void_p(x)
    ctypes.windll.psapi.GetModuleFileNameExA(p, x, buf, len(buf))
    return buf.value.split('\\')[-1].lower()


class Process(c_int):

    def threads(self):
        TH32CS_SNAPTHREAD = 4
        h = windll.kernel32.CreateToolhelp32Snapshot(
            TH32CS_SNAPTHREAD, self.value)
        entry = THREADENTRY32()
        entry.dwSize = 0x1c
        windll.kernel32.Thread32First(h, byref(entry))
        z = []
        if entry.th32OwnerProcessID == self.pid:
            z.append(entry.th32ThreadID)
        while windll.kernel32.Thread32Next(h, entry):
            if entry.th32OwnerProcessID == self.pid:
                z.append(entry.th32ThreadID)
            pass
        return z

    def hook(self, lib, name, code):
        z = c_long(0)
        c = asm(code)
        d = va(self.value, 0, 0x1000, 0x3000, 0x40)
        m = self.modules()
        a = addr(c_void_p(m[lib]), name)

        # allocate hook code
        vp(c_void_p(a & 0xfffffffffffff000), 0x1000, 0x40, byref(z))
        self.write(d, c)

        # jmp [rip-14]. Works for most WINAPIs.
        self.write(a - 8, struct.pack("<Q", d))
        self.write(a, "\xFF\x25\xF2\xFF\xFF\xFF")

    @staticmethod
    def attach(pid):
        proc = Process()
        proc.value = ctypes.windll.kernel32.OpenProcess(
            PROCESS_ALL_ACCESS, False, pid)
        proc.pid = pid
        return proc

    def write(self, addr, str):
        z = c_long(0)
        return wpr(self.value, c_void_p(addr), str, len(str), byref(z))

    def __trunc__(self):
        return self.value

    def modules(self):
        m = (c_longlong * 1000)()
        y = c_long(0)
        l = ctypes.windll.psapi.EnumProcessModules(self.value, m, 1000 * 8, byref(y))
        m = list(m)[:y.value / 8]
        m = {_addr_to_module(self.value, x): x for x in m}
        return m
