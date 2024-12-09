import itertools
import struct


def g0(x15_a5):
    _59 = 0xFFFFFFFFFFFFFFC5
    loc54 = 0x9282F38FD9DE6BB
    loc55 = x15_a5
    loc57 = 0

    while loc54 > 0:
        loc56 = loc54 & 0x1
        loc58 = loc55 * loc56
        loc62 = loc57 + loc58
        loc62, loc61 = loc62 & 0xFFFFFFFF, loc62 >> 32
        loc59 = 0xFFFFFFFFFFFFFFFF % _59
        loc59 = ((loc59 + 1) * loc61) % _59
        loc60 = loc62 % _59
        loc60 = (loc60 + loc59) % _59
        loc57 = loc60
        loc54 >>= 1

        loc66 = loc55 * 2  # Equivalent to loc55 + loc55
        loc66, loc65 = loc66 & 0xFFFFFFFF, loc66 >> 32
        loc63 = 0xFFFFFFFFFFFFFFFF % _59
        loc63 = ((loc63 + 1) * loc65) % _59
        loc64 = loc66 % _59
        # add_i64 loc64,loc64,loc63
        loc64 = (loc64 + loc63) % _59
        loc55 = loc64

    loc70 = loc57 + 0x9A10A8B923AC8BF
    loc70, loc69 = loc70 & 0xFFFFFFFF, loc70 >> 32
    loc67 = 0xFFFFFFFFFFFFFFFF % _59
    loc67 = ((loc67 + 1) * loc69) % _59
    loc68 = loc70 % _59
    return (loc68 + loc67) % _59


def g0_1(x15_a5):
    MODULO = 0xFFFFFFFFFFFFFFC5  # Equivalent to 2^64 - 59
    loc54 = 0x9282F38FD9DE6BB  # Fixed constant
    loc55 = x15_a5  # Multiplicand
    loc57 = 0  # Accumulator

    while loc54 > 0:
        if loc54 & 1:  # If the least significant bit of loc54 is set
            loc57 = (loc57 + loc55) % MODULO
        loc55 = (loc55 * 2) % MODULO  # Double loc55 and reduce modulo
        loc54 >>= 1  # Shift loc54 right by 1 bit

    loc57 = (loc57 + 0x9A10A8B923AC8BF) % MODULO  # Final adjustment
    return loc57


def g0_2(x15_a5):
    MODULO = 0xFFFFFFFFFFFFFFC5  # Equivalent to 2^64 - 59
    loc54 = 1506885014147991363  # Fixed constant
    loc55 = (x15_a5 + 17752896661547726598) % MODULO
    loc57 = 0  # Accumulator

    while loc54 > 0:
        if loc54 & 1:  # If the least significant bit of loc54 is set
            loc57 = (loc57 + loc55) % MODULO
        loc55 = (loc55 * 2) % MODULO  # Double loc55 and reduce modulo
        loc54 >>= 1  # Shift loc54 right by 1 bit

    return loc57


def pbox(x14, x15):
    result = x15

    for i in range(0x10):  # Loop L3
        selector = (x14 >> (i * 4)) & 0x7
        transformed = 0

        for j in range(0x8):  # Loop L4
            element = j
            if j == 0:
                element = selector
            if j == selector:
                element = 0

            byte = (result >> (element * 8)) & 0xFF
            transformed |= (byte << (j * 8))

        result = transformed

    return result



def extract_index(a3):
    v7 = 3
    v8 = 3
    for v6 in range(a3):
        v8 = 3 * v7 % 29
        v7 = v8
    return v8


x = 0x617B4E4F43434553
a = g0(x)
b = g0_1(x)
c = g0_2(b)
print(hex(a), hex(b), hex(c))
boxes = [0xc1258110b8c51f9e, 0xa86354f8bb35d35f, 0xb16ccb3f4d5c8018, 0x803ed074b4320ba0, 0x34968cd63f4d48d8, 0xad4ff2ab83fd411, 0x2672cbe8244c67f, 0x21d302f1ce581e42, 0x5086382319de92ef, 0xc41f9ce7c6ca8eba, 0xd534200bc7247ff9, 0xe424883534b75239, 0x104a93f53bc6efa1, 0x912999c2cff3cf13, 0x78178bd0998bc480, 0x7e7d4c73b8ffb2b8, 0xcba80bb864516e5d, 0xe5bbcf766ca25ce9, 0x87bbce79c172df5, 0x23cb304feee9a0c7, 0xcac09104b6bbde7e, 0xeed6fe5fc72ee54d, 0xc330d82edd4c152f, 0xb55228f811aa127, 0xc8cb484145d835d2, 0xf62d689de9a1384a, 0xf2fe357076301ca7, 0xb701b9064b5bbd38, 0x4418934968af30d3]
arr = [extract_index(i) for i in range(10)]
print(arr, len(arr), len(set(arr)))
arr = [boxes[i] for i in arr]
print(arr)
# Impossible to reverse pbox since it's shuffling with input key
flag = b''
for index, x in enumerate(arr):
    x = g0_2(x)
    for perm in itertools.permutations(range(8)):
        y = 0
        for i in range(8):
            y |= ((x >> (perm[i] * 8)) & 0xFF) << (i * 8)
        y = g0_2(y)
        if y & 0x7f7f7f7f7f7f7f7f == y:
            bytes_ = struct.pack("<Q", y)
            if all(0x30 <= b < 0x3a or b in b'SECCON{}' or 0x61 <= b <= 0x7a or b == 0 for b in bytes_) and all(b not in bytes_ for b in b';%@|_?^<>'):
                print(index, x, bytes_)
                res = bytes_
    flag += res
print(flag.decode())
print(hex(pbox(0x617B4E4F43434553, 0x14728e20b522591)))