#!/usr/bin/env python

"""
    Copyright (C) 2012 Bo Zhu http://about.bozhu.me

    Permission is hereby granted, free of charge, to any person obtaining a
    copy of this software and associated documentation files (the "Software"),
    to deal in the Software without restriction, including without limitation
    the rights to use, copy, modify, merge, publish, distribute, sublicense,
    and/or sell copies of the Software, and to permit persons to whom the
    Software is furnished to do so, subject to the following conditions:

    The above copyright notice and this permission notice shall be included in
    all copies or substantial portions of the Software.

    THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
    IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
    FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL
    THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
    LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
    FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER
    DEALINGS IN THE SOFTWARE.
"""


def KSA(key):
    keylength = len(key)

    S = range(256)

    j = 0
    for i in range(256):
        j = (j + S[i] + key[i % keylength]) % 256
        S[i], S[j] = S[j], S[i]  # swap

    return S


def PRGA(S):
    i = 0
    j = 0
    while True:
        i = (i + 1) % 256
        j = (j + S[i]) % 256
        S[i], S[j] = S[j], S[i]  # swap

        K = S[(S[i] + S[j]) % 256]
        yield K


def RC4(key):
    S = KSA(key)
    return PRGA(S)


if __name__ == '__main__':
    # test vectors are from http://en.wikipedia.org/wiki/RC4

    # ciphertext should be BBF316E8D940AF0AD3
    plaintext = 'Plaintext'

    table = list(bytearray(open('table.bin', 'rb').read()))

    # ciphertext should be 1021BF0420
    #key = 'Wiki'
    #plaintext = 'pedia'

    # ciphertext should be 45A01F645FC35B383552544B9BF5
    #key = 'Secret'
    #plaintext = 'Attack at dawn'

    v0 = bytearray(range(36))
    v2 = [0] * 36
    v1 = [0] * 36

    msb = lambda x: x >> 4
    lsb = lambda x: x & 0xf
    
    # r = []
    # for i in range(72):
    #     if ( i <= 35 ):
    #         if ( table[i] & 1 ):
    #             x = v2[i % 36] = msb(v0[table[i] / 2]);
    #         else:
    #             x = v2[i % 36] = lsb(v0[table[i] / 2]);
    #     else:
    #         if ( table[i] & 1 ):
    #             x = v1[i % 36] = msb(v0[table[i] / 2]);
    #         else:
    #             x = v1[i % 36] = lsb(v0[table[i] / 2]);
    #     if i & 1:
    #         handler = msb
    #     else:
    #         handler = lsb
    #     r.append(handler(v0[i / 2]))
    # print r

    ciphertext = bytearray(open('flag_enc', 'rb').read())

    f1, f2 = None, None
    x = range(100000) # pid range bruteforce
    for i in x:
        keystream = RC4(bytearray('%d' % i))
        keystream2 = RC4(bytearray('%d' % i))
        h1 = [x^y for x, y in zip(keystream, ciphertext[:0x24])]
        h2 = [x^y for x, y in zip(keystream2, ciphertext[0x24:])]
        if all(x<16 for x in h1):
            print 'ey', i
            f1 = h1
        if all(x<16 for x in h2):
            print 'ey', i
            f2 = h2
    
    flag = [None] * 0x48
    f = f1 + f2

    # f = v2 + v1

    print f

    for i in range(len(flag)):
        x = table[i] ^ 1
        flag[x] = f[i]

    print flag

    flag = ''.join(bin(x)[2:].zfill(4) for x in flag)
    from hexdump import hexdump
    flag = [int(flag[i:i+8], 2) for i in range(0, len(flag), 8)]
    flag = bytearray(flag)
    flag = str(flag)
    hexdump(flag)

    print flag