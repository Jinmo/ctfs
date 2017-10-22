from z3 import *

data = open(r'C:\Users\berry\Downloads\TirpleRotate\encrypt', 'rb').read().strip()

data = data.split(' ')
print data
data = map(int, data)
size = len(data)
print size
m = [[0] * size for i in range(3)]

def c1(a1, a2):
  for i in range(a2 - 23):
    a1[i + 23] = a1[i + 5] ^ a1[i];

def c2(a1, a2):
  for i in range(a2 - 24):
    a1[i + 24] = a1[i + 1] ^ a1[i + 3] ^ a1[i + 4] ^ a1[i];

def c3(a1, a2):
  for i in range(a2 - 25):
    a1[i + 25] = a1[i + 3] ^ a1[i];

v3 = [0]  * 4
v3[0] = 0;
v3[1] = 23;
v3[2] = 24;
v3[3] = 25;
a2 = [BitVec('input[%d]' % i, 8) for i in range(size)]
input = list(a2)

bits = [0] * 72
for i in range(72):
    bits[i] = (a2[i / 8] >> (7 - i % 8)) & 1;
v6 = 0;
offset = 0

for j in range(3):
    v6 += v3[j];
    for k in range(v3[j + 1] - 1, -1, -1):
        m[j][k] = bits[offset];
        offset += 1

for j in range(3):
    [c1, c2, c3][j](m[j], size)

v3 = [0] * size
for k in range(size):
    v3[k] = m[1][k] & m[2][k] ^ m[1][k] & m[0][k] ^ m[2][k];


print v3[0]

s = Solver()
for i in range(size):
    s.add(v3[i] == data[i])

print s.check()
model = s.model()
print bytearray([model[input[i]].as_long() for i in range(9)])