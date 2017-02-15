from z3 import *
import hashlib
import struct

def md5(x):
  return
  print hashlib.md5(str(bytearray(x))).hexdigest()
def decrypt(a1, key):
  v4 = {i: 0 for i in range(7)}
  v9 = {i: 0 for i in range(10)}
  key = {i: key[i] for i in range(len(key))}
  md5(a)

  _4 = 4;
  v18 = 5;
  _3 = 3;
  _10 = 10;
  _5 = 5;
  _7 = 7;
  offset = 0;
  v15 = len(a);
  v7 = {i: 0 for i in range(5)}
  for i in range(0, len(a) - len(a) % _7, _7 ):
    for j in range (0, _3):
      v4[j] = a1[j + offset];
    for j in range(0, _7 - _3):
      v4[(j + _3)] = a1[_3 + v15 - _7 + j];
    for j in range(0, _7):
      v4[j] ^= key[j];
    for j in range(0, _3):
      a1[j + offset] = v4[(j + _7 - _3)];
    for j in range(0, _7 - _3):
      a1[_3 + v15 - _7 + j] = v4[j];
    offset += _3;
    v15 -= _7 - _3;
    _3 += 2;
    if ( _3 == 9 ):
      _3 = 3;
  offset = 0;
  v15 = len(a);
  for i in range(0, len(a) - len(a) % _5, _5 ):
    for j in range(0, v18):
      v7[j] = a1[j + offset];
    for j in range(0, _5 - v18):
      v7[j + v18] = a1[v18 + v15 - _5 + j];
    for j in range(0, _5):
      v7[j] ^= key[2 * j + 1];
    for j in range(0, v18):
      a1[j + offset] = v7[j + _5 - v18];
    for j in range(0, _5 - v18):
      a1[v18 + v15 - _5 + j] = v7[j];
    md5(a1)
    offset += v18;
    v15 -= _5 - v18;
    v18 -= 1
    if ( v18 == 0 ):
      v18 = 5;
  offset = 0;
  v15 = len(a);
  for i in range( 0, len(a) - len(a) % _10, _10 ):
    for j in range(0, _4):
      v9[j] = a1[j + offset];
    for j in range(0, _10 - _4):
      v9[j + _4] = a1[_4 + v15 - _10 + j];
    for j in range(0, _10):
      v9[j] ^= key[j];
    for j in range(0, _4):
      a1[j + offset] = v9[j + _10 - _4];
    for j in range(0, _10 - _4):
      a1[_4 + v15 - _10 + j] = v9[j];
    offset += _4;
    v15 -= _10 - _4;
    _4 += 1
    if ( _4 == 9 ):
      _4 = 4;
  offset = 0;
  v15 = len(a);
  _4 = 4;
  for i in range( 0, len(a) - len(a) % _10, _10 ):
    for j in range(0, _4):
      v9[j] = a1[j + offset];
    for j in range(0, _10 - _4):
      v9[j + _4] = a1[_4 + v15 - _10 + j];
    for j in range(0, _10):
      v9[j] ^= key[j];
    for j in range(0, _4):
      a1[j + offset] = v9[j + _10 - _4];
    for j in range(0, _10 - _4):
      a1[_4 + v15 - _10 + j] = v9[j];
    offset += _4;
    v15 -= _10 - _4;
    _4 += 1
    if ( _4 == 9 ):
      _4 = 4;
  print len(a), v4.keys(), v9.keys(), v7.keys()
  return [a1[i] for i in range(len(a))]

a = [241, 100, 114, 74, 79, 72, 77, 186, 119, 115, 29, 52, 245, 175, 184, 15, 36, 86, 17, 101, 71, 163, 47, 115, 164, 86, 79, 112, 74, 19, 87, 156, 63, 111, 6, 97, 64, 144, 175, 57, 16, 41, 52, 195, 0, 122, 64, 61, 78, 63, 14, 42, 47, 32, 127, 115, 137, 125, 75, 29, 9, 170, 208, 0, 33, 137, 77, 42, 103, 124, 24, 59, 57, 242, 141, 28, 167, 113, 87, 46, 49, 20, 103, 72, 60, 125, 175, 112, 174, 16, 49, 104, 209, 38, 5, 200, 37, 242, 98, 245, 93, 56, 52, 242, 32, 14, 126, 159, 251, 87, 114, 38, 87, 103, 21, 16, 21, 19, 185, 62, 121, 137, 93, 36, 18, 1, 152, 123, 24, 37, 224, 223, 124, 36, 27, 45, 68, 176, 16, 61, 87, 61, 98, 180, 33, 29, 62, 209, 16, 215, 69, 116, 150, 43, 109, 59, 237, 16, 0, 103, 49, 223, 108, 184, 134, 26, 124, 107, 100, 120, 198, 55, 118, 230, 97, 160, 173, 190, 76, 186, 167, 13]
b = [0] * 7
v5 = b
v5[0] = 0x2A4D48734AD94861;
v5[1] = 0x6773AFF5A5187C07;
v5[2] = 0xC7002ACCB8595624;
v5[3] = 0x2439342338DF6F95;
v5[4] = 0xEC833245186E4F5C;
v5[5] = 0x6F14A0004A585BB5;
v5[6] = 0xDA72C4CBEADBE24;
b = list(bytearray(struct.pack("<7Q", *b)))
print b, len(b)
orig = key = [BitVec('key[%d]' % i, 8) for i in range(10)]

data = decrypt(a, key)
#data2 = decrypt(b, key)
s = Solver()
prefix = '55 48 89 E5 48'.replace(' ', '').decode('hex')
prefix = bytearray(prefix)
suffix = [0xc9, 0xc3]
for i in range(len(prefix)):
  s.add(data[i] == prefix[i])

for i in range(len(suffix)):
  s.add(data[-i - 1] == suffix[-i - 1])

print s

blacklist = '{}()"\'[]`'
blacklist = bytearray(blacklist)
for i in range(len(key)):
  s.add(key[i] > 32)
  s.add(key[i] < 127)
  for c in blacklist:
    s.add(key[i] != c)
#for i in range(len(data2)):
#  s.add(data2[i] > 0)

for c in bytearray('/.-!,;()'):
  s.add(key[2] != c)

s.add(key[2] == ord('3'))
s.add(key[4] == ord('7'))

target = struct.pack("<2Q", 0x618F652224A9469F, 0x14B97D8EE7DE0DA8).encode('hex')
while True:
  if s.check() == sat:
    key_ = [s.model()[key[i]].as_long() if s.model()[key[i]] is not None else 1 for i in range(len(key))]
    key_ = bytearray(key_)
    hash = hashlib.md5(key_).hexdigest()
    print key_
    if hash == target:
      print 'good', key_
      exit()
    payload = []
    for i, c in enumerate(key_):
      payload.append(key[i] != c)
    s.add(Or(*payload))
  else:
    print 'unsat'
    exit()