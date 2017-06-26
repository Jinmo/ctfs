from z3 import *

def hash1(a1):
    v8 = 0
    for x in a1:
        v6 = x
        v8 = v6 ^ ((v8 >> 30) | (v8 << 7) & 0xDEADBEAF)
    return v8

def hash2(a1):
    result = ((((((a1[0] - 0x2EA15A13) ^ ((a1[3] << 24) | (a1[2] << 16) | (a1[1] << 8) & a1[0])) + a1[1]) | (a1[0] << 24) & (a1[3] << 16) | (a1[2] << 8) | a1[1]) \
             + a1[2]) & ((a1[1] << 24) | (a1[0] << 16) ^ ((a1[3] << 8) | a1[2]))) \
           + a1[3];
    v4 = result ^ ((a1[2] << 24) | (a1[1] << 16) | (a1[0] << 8) ^ a1[3]);
    return v4

def int32(x):
    if x & 0x80000000:
        x -= 2 ** 32
    return x

t1 = [76297767L, 109647920L, 67639907L, 67909172L, 76101665L]
t2 = [1578124050L, 1342719088L, 369641700L, 1326534510L, 306925392L]
t2 = map(int32, t2)
flag = ''
for j in range(len(t1)):
    s = Solver()
    text = [BitVec('x[%d]' % i, 32) for i in range(4)]
    for i in range(len(text)):
        s.add(text[i] < 127)
        s.add(text[i] >= 0)
    s.add(hash1(text) == t1[j])
    s.add(hash2(text) == t2[j])
    if s.check() == unsat:
        print 'nope'
        exit()
    print s.model()
    flag += bytearray([s.model()[text[i]].as_long() for i in range(len(text))])
    print `flag`

print flag