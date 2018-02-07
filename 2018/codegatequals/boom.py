# Rotate left: 0b1001 --> 0b0011
rol = lambda val, r_bits, max_bits=32: \
    (val << r_bits%max_bits) & (2**max_bits-1) | \
    ((val & (2**max_bits-1)) >> (max_bits-(r_bits%max_bits)))

# Rotate right: 0b1001 --> 0b1100
ror = lambda val, r_bits, max_bits=32: \
    ((val & (2**max_bits-1)) >> r_bits%max_bits) | \
    (val << (max_bits-(r_bits%max_bits)) & (2**max_bits-1))

box = [ror(ror(ror(c, 3) ^ 0x62, 5) ^ 0x32, 7) % 47 for c in range(100)]

print "Know what? It's a new day~"

sbox = 'f7*zq5$ase0t6ui#^yd2owgb_n8pu4!k&vc@lrj19mx3h'
for x in ('carame1', 'w33k3end', 'pand0ra')[2:]: # pand0ra only
  l = []
  for c in bytearray(x): 
    i = sbox.find(chr(c))
    if i == -1:
      print 'wtf'
      exit()
    c = i
    c = box.index(c)
    l.append(c)
  print ' '.join(map(str, l))

# print 'wow'
print 0x0000000000000011, 0x0000000000000018, 0x0000000000000001, 0x0000000000000008, 0x000000000000000f, 0x0000000000000017, 0x0000000000000005, 0x0000000000000007, 0x000000000000000e, 0x0000000000000010, 0x0000000000000004, 0x0000000000000006, 0x000000000000000d, 0x0000000000000014, 0x0000000000000016, 0x000000000000000a, 0x000000000000000c, 0x0000000000000013, 0x0000000000000015, 0x0000000000000003, 0x000000000000000b, 0x0000000000000012, 0x0000000000000019, 0x0000000000000002, 0x0000000000000009

# print 'lil_break'
def func(a1, a2):

  while True:
    if ( a2 == 1 ):
      a1 = a1 + 1;
      break
    elif ( a2 % 2 ):
      a2 = 3 * a2 + 1;
      a1 = a1 + 1
    else:
      a1 = a1 + 1
      a2 = a2 / 2
  return a1;

for i in range(1, 100):
  if func(0, i) == 107:
    print i
    break

# print 'gogo'
print 1, 1, 1, 1