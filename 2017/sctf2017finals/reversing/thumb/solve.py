from z3 import *
import struct

rand_table = [0] * 1000
table = [[0] * 16 for i in range(16)]

f = open('stream', 'rb')
def rand():
    global f
    return struct.unpack("<L", f.read(4))[0]

input = []

from pprint import pprint

for i in range(16):
    for j in range(16):
      table[i][j] = BitVecVal(rand() & 0xff, 8)

for i in range(34):
    input.append(BitVec('input[%d]' % len(input), 8))
    v1 = input[-1];
    v2 = rand() & 0xF;
    v3 = rand() & 0xF;
    table[v2][v3] ^= v1;

def sub_103C0(result, a2):
  for i in range(16):
    table[result][i], table[a2][i] = table[a2][i], table[result][i];

def rotate_right(result, a2):
  v4 = 0;
  for i in range(16):
    v2 = (table[result][i]) << (8 - a2);
    table[result][i] = v4 | LShR(table[result][i], a2);
    v4 = v2;
  table[result][0] |= v4;

def sub_104F0(target_row, a2, a3):

  for row in range(16):
    table[row][a2] ^= a3;
    table[target_row][row] ^= a3;

def swapcolumn(x, y):
  for row in range(16):
    table[row][x], table[row][y] = table[row][y], table[row][x];

for i in range(1000):
    v1 = rand() & 0xF;
    v2 = rand() & 0xF;
    sub_103C0(v1, v2);
for j in range(1000):
    v3 = rand() & 0xF;
    v4 = rand() & 7;
    rotate_right(v3, v4);
for k in range(1000):
    v5 = rand() & 0xF;
    v6 = rand() & 0xF;
    v7 = rand() & 0xff;
    sub_104F0(v5, v6, v7);
for l in range(1000):
    v8 = rand() & 0xF;
    v9 = rand() & 0xF;
    swapcolumn(v8, v9);

target = [63, 177, 191, 82, 152, 136, 53, 157, 41, 61, 168, 73, 162, 168, 75, 195, 235, 104, 38, 206, 13, 73, 254, 8, 205, 37, 115, 100, 78, 120, 245, 234, 23, 86, 221, 238, 47, 76, 198, 11, 156, 5, 64, 142, 119, 36, 244, 2, 183, 12, 210, 173, 237, 8, 24, 42, 202, 238, 212, 42, 114, 166, 19, 198, 88, 245, 124, 39, 172, 129, 15, 19, 199, 20, 78, 167, 140, 81, 9, 138, 222, 2, 20, 126, 157, 142, 220, 104, 34, 119, 20, 196, 248, 194, 196, 102, 191, 9, 35, 47, 210, 141, 221, 127, 160, 163, 137, 71, 230, 4, 107, 252, 135, 50, 72, 13, 172, 89, 159, 13, 221, 207, 47, 96, 195, 61, 54, 203, 35, 182, 0, 84, 145, 90, 197, 74, 124, 147, 223, 254, 245, 30, 99, 212, 110, 157, 155, 133, 99, 68, 252, 163, 227, 0, 212, 34, 181, 218, 219, 126, 29, 38, 68, 94, 18, 88, 57, 132, 106, 123, 44, 179, 76, 69, 19, 31, 187, 45, 223, 149, 195, 244, 3, 125, 110, 180, 181, 204, 183, 234, 15, 89, 204, 237, 107, 64, 67, 124, 81, 121, 132, 37, 154, 76, 192, 120, 10, 191, 246, 47, 85, 141, 153, 106, 75, 51, 188, 235, 30, 145, 107, 82, 50, 13, 253, 138, 124, 148, 95, 1, 43, 200, 169, 168, 177, 160, 0, 32, 80, 31, 106, 110, 47, 70, 246, 21, 35, 148, 87, 210, 86, 156, 156, 75, 81, 189]

s = Solver()
for i in range(16):
    for j in range(16):
        s.add(table[i][j] == target[i * 16 + j])

for i in range(len(input)):
    s.add(input[i] > 31)
s.add(input[len('SCTF{t1')] != ord('K'))
s.add(input[len('SCTF{t1')] != ord('+'))
s.add(input[len('SCTF{t1')] != ord('k'))
s.add(input[len('SCTF{t1')] == ord('n'))

print s.check()
print s.model()
model=s.model()
print bytearray([model[x].as_long() for x in input])

















