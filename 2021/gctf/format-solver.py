import struct, sympy
dword_51D4 = [0] * 7
dword_51D4[6] = 0xE8680215
dword_51D4[5] = 0xE6F62831
dword_51D4[4] = 0xD531548
dword_51D4[3] = 0x79798688
dword_51D4[2] = 0x6F57A0A3
dword_51D4[1] = 0x8AA5C4A9
dword_51D4[0] = 0xF9CFCCF5
target=[struct.pack("<L", x) for x in dword_51D4]
target=b''.join(target)
primes = list(x for x in sympy.primerange(13200, 13600))
print(primes)
def _(x):
    regs = [x]
    def recursive():
      if ( regs[0] == 1 ):
        regs[0] = 0;                                # return 0
      elif ( regs[0] - 1 > 0 ):
        if ( (regs[0] & 1) == 0 ):
          regs[0] //= 2;
        else:
          regs[0] = 3 * regs[0] + 1;
        recursive();
        regs[0] += 1;
    recursive()
    return regs[0]
print(bytearray([(x&0xff)^(y-_(i) & 0xff) for x, y, i in zip(primes, target, range(1, len(target) + 1))]))