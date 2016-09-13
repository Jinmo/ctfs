r = [0] * 50

for i in range(256):
  r[50 - 33] = r[50 - 4];
  r[50 - 36] = r[50 - 4];
  r[50 - 35] = i + ord('D');
  r[50 - 34] = i + ord(':');
  r[50 - 32] = i + ord('=');
  r[50 - 31] = i + ord('r');
  r[50 - 12] = i + ord('t');
  r[50 - 30] = i + ord('[');
  r[50 - 29] = i + ord('X');
  r[50 - 28] = i + ord('k');
  r[50 - 27] = i + ord('X');
  r[50 - 26] = i + ord('c');
  r[50 - 25] = i + ord('f');
  r[50 - 24] = i + ord('j');
  r[50 - 23] = i + ord('j');
  r[50 - 22] = i + ord('n');
  r[50 - 21] = i + ord('f');
  r[50 - 20] = i + ord('e');
  r[50 - 19] = i + ord('k');
  r[50 - 18] = i + ord('j');
  r[50 - 17] = i + ord('k');
  r[50 - 16] = i + ord('f');
  r[50 - 15] = i + ord('g');
  r[50 - 14] = i + ord('l');
  r[50 - 13] = i + 106;
  print `bytearray(x & 0xff for x in r).strip('\x00').rstrip('\x00')`