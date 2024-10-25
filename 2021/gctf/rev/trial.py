from z3 import *
arr = open('mem', 'rb').read()
input = [BitVec('input%d' % i, 8) for i in range(27)]
i = 0
l = 0
A = 0
B = 1
found = True
s = Solver()
for i in range(27):
    j = input[i] * (arr[i])
    A, B = B, A + B & 0xff
    l += arr[i+32] ^ (j + A)
    print(l)
    s.add(arr[i + 64] == l)
    l = arr[i + 64]
    assert s.check() == sat
    print([s.model()[input[i]] for i in range(i + 1)])

print(bytes([s.model()[input[i]].as_long() for i in range(i + 1)]))