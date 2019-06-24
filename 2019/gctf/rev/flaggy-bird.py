from Crypto.Cipher import AES
from hashlib import sha256
import sys

blacklisted = [0x00000000, 0x00000000, 0x00000000, 0x00000000, 0x00000001, 0x00000000, 0x00000000, 0x00000001, 0x00000000, 0x00000001, 0x00000001, 0x00000001, 0x00000001, 0x00000000, 0x00000000, 0x00000000, 0x00000001, 0x00000001, 0x00000000, 0x00000000, 0x00000001, 0x00000000,
               0x00000001, 0x00000000, 0x00000000, 0x00000000, 0x00000001, 0x00000001, 0x00000001, 0x00000000, 0x00000000, 0x00000000, 0x00000001, 0x00000000, 0x00000000, 0x00000000, 0x00000000, 0x00000001, 0x00000001, 0x00000001, 0x00000001, 0x00000001, 0x00000000, 0x00000001, 0x00000000]
visited = set()


class Error(Exception):
    def __init__(self, *args):
        self.data = args
        # print repr(self.data)[1:-1]
        # print visited

    def __str__(self):
        return repr(self.data)[1:-1]


class Slice:
    def __init__(self, data, offset, size):
        if isinstance(data, Slice):
            self.data = data.data
            self.offset = data.offset + offset
        else:
            self.data = data
            self.offset = offset
        self.size = size

    def __getitem__(self, offset):
        visited.add(self.offset + offset)
        return self.data[self.offset+offset]

    def __setitem__(self, offset, value):
        visited.add(self.offset + offset)
        self.data[self.offset+offset] = value

    def __repr__(self):
        return 'Slice(%r, offset=%r, %r)' % (self.data[:self.size], self.offset, self.size)


valid = True
p = 0


def M(dest, size):
    global p
    res = [-1] * size
    if (size >= 2):
        mid = size >> 1
        M(dest, size >> 1)
        if (valid):
            remain = size - mid
            mid_ = Slice(dest, mid, remain)
            M(mid_, size - mid)
            if (valid):
                i = 0
                j = 0
                out = 0
                if (remain > 0):
                    out = 0
                    orig = p
                    while (1):                           # insertion sort
                        cur = mid_[i]
                        if (dest[j] >= cur):
                            if dest[j] == cur:
                                raise Error('left == right', mid_, size, i, j)
                            if (blacklisted[p]):
                                mid_[i], dest[j] = dest[j], mid_[i]
                                # print 'right < left', dest
                                raise Error('right < left', mid_, size, i, j)
                            res[out] = mid_[i]
                            i += 1
                        else:
                            if (blacklisted[p] != 1):
                                mid_[i], dest[j] = dest[j], mid_[i]
                                raise Error('left > right', mid_, size, i, j)
                            res[out] = dest[j]
                            j += 1
                        p += 1
                        out += 1
                        if (j >= mid or i >= remain):
                            break
                # print i, j, mid_,
                if (j < mid):
                    for _ in range(mid - j):
                        res[out + _] = dest[j + _]
                    out = out + mid - j
                if (i < remain):
                    for _ in range(size - (mid + i)):
                        res[out + _] = dest[mid + i + _]
                for _ in range(size):
                    dest[_] = res[_]


target = [9, 8, 7, 2, 11, 15, 13, 10, 6, 5, 14, 4, 3, 0, 12, 1]

if target is None:
    yo = range(16)
    p = 0
    for i in range(640000):
        valid = True
        p = 0
        try:
            ey = yo[:]
            M(yo, 16)
            print 'done'
            target = ey
            break
        except Error as e:
            if i % 32000 == 0:
                print yo, e

print reduce(lambda x, y: x * (y + 1), target, 1)
iv = str(bytearray(x & 0xff for x in [-30, 1, 9, -29, -92,
                                      104, -52, -82, 42, -116, 1, -58, 92, -56, -25, 62]))
for i in range(2**16):
    yo = bin(i)[2:].zfill(16)
    T = [0]*32
    for j in range(16):
        T[j*2+int(yo[j])] = target[j]
    data = sha256(str(bytearray(T)))
    digest = bytearray(x & 0xff for x in [46, 50, 92, -111, -55, 20, 120, -77, 92, 46, 12, -74, 91,
                                          120, 81, -58, -6, -104, -123, 90, 119, -61, -65, -45, -16, 8, 64, -68, -103, -84, -30, 107])
    if data.hexdigest() == str(digest).encode('hex'):
        data = AES.new(str(bytearray(T)), AES.MODE_CBC, IV=iv).decrypt(str(bytearray(x & 0xff for x in [-113, -47, -15, 105, -18, 14, -118, 122, 103, 93, 120, 70, -36, -82, 109, 113, 36, -127, 19, -35, -68, 21, -20, -69, 7, 94, -115, 58, -105, -10, -77, -62, 106, 86, -44, -24, -46, 112, 37, 3, -34, -51, -35, 90, -93, -59, 12, -35, 125, -33, -6, -109, -100, 25, 127, 126, -81, -73, -50, -61, 84, 32, 127, -126, -81, -20, -116, -82, 38, 119, 27, 7, 122, -2, -30, 58, 98, -17, 66, -103, 116, -83, -36, 106, 121, -23, -40, 125, -27, -37, -95, -59, -70, 61, 71, 43, -55, -22, -8, -72, 50, -19, -77, 37, 78, -37, 126, 119, 31, -37, 70, 41, 64, -97, -28, 68, -14, -41, -17, -94, 3, 2, 31, -85, -86, 84, -34, -58, 115, -14, 87, 62, 52, 103, -28, -89, 3, 104, 19, 61, -7, -53, -15, 28, -108, -85, -106, 3, -77, -11,
                                                                                                        37, -65, -107, -61, 53, -3, -68, 105, -101, -118, -44, 69, -63, -81, -57, 74, -86, 76, 27, -58, 91, 64, 60, -86, 3, 5, -108, -44, 77, -80, 50, 119, 109, 107, -43, -93, -87, -42, 32, 66, 27, -64, 38, -44, 50, -108, -21, -70, -102, -63, -120, 118, 7, 89, -106, 66, -3, -10, 93, -9, 3, 13, 35, 37, -19, 116, 47, 29, 91, -30, 69, -49, 109, 72, 6, 36, 58, -63, 107, 48, 70, 127, -127, 51, -110, 48, -73, -62, -118, 59, -27, 30, -109, -42, -109, -54, -22, 95, 123, -89, -62, -99, -62, 66, 60, 126, -52, -117, -98, -95, 2, -93, -93, -30, 85, -113, -77, -60, -83, -4, -50, 52, 113, 62, -104, -124, 56, 89, -62, 108, 35, -10, 90, -42, -26, 114, 11, -49, -18, 56, -60, -87, -118, -106, -76, -103, -53, -7, -54, -70, -120, -92, -29, -17, -106, 80, -3, -18, -44, 115, -31, 57, -57, 60, 94, -6, 18, -56, -27, -17])))
        data = data[:-ord(data[-1])]
        print `data`
        open('result', 'wb').write(data)
        import zlib
        from PIL import Image
        image = Image.new('RGB', (190, 46))
        data = data.decode('zlib')
        for i in range(190):
            for j in range(46):
                image.putpixel((i, j), 0xffffff if data[j*190+i] == '0' else 0)
        image.save('1.png')
        data = ''.join('.' if x == '0' else '#' for x in data)
        data = [data[i:i+190] for i in range(0, 46 * 190, 190)]
        print '\n'.join(data)
        break
print '\n'.join(data).replace('0', '_')
