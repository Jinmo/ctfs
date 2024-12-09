from z3 import *
import struct
res = [BitVec('x%d'%i, 32) for i in range(8)]


def get(offset):
    assert offset % 4 == 0
    return res[offset // 4]

offset = 0
s = Solver()
s.add((get(offset) == 1128482131))

offset = 4
s.add(((get(offset) ^ 0xDEADBEEF) == -338235232))

offset = 8
s.add(((get(offset) ^ 0xCAFEBABE) == -107639082))

offset = 12
s.add(((get(offset) ^ 0xC0FFEE) == 1605684913))

offset = 16
s.add((get(offset) + get(offset - 4) == -1798069804))

offset = 20
s.add((get(offset) + get(offset - 4) == -1651204643))

offset = 24
s.add((get(offset) + get(offset - 4) == -1650629995))

offset = 28
s.add((get(offset) - get(offset - 4) == 1204500027))

assert s.check() == sat
m = s.model()
print(b''.join([struct.pack("<L", m[res[i]].as_long()) for i in range(8)]))