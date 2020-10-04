data = open('ww.wasm', 'rb').read()
needle = bytes.fromhex('9A B6 A9 E9 95 CF BE DC B7 ED CB F3 9B 7A 36 68')
pos = data.find(needle)
size = 0x5200
arr = open('data2.wasm', 'rb').read()
end = bytes.fromhex('66 6C 61 67 7B 73 65 63 72 65 74 2B 00 7D 0A 00')
arr = arr[:arr.find(end) + len(end)]
print(hex(len(arr)))
arr = bytearray(arr.ljust(size, b'\x00'))
assert len(arr) == 0x5200
key = b'eNj0y_weba5SemB1Y.lstrip("web")!'
for j in range(0, len(arr), 512):
    state = 0xff
    for i in range(j, j+512):
        v11 = i & 0x1F
        v7 = key[v11] ^ (arr[i]+v11) ^ state
        arr[i] = v7 & 0xff
        state = arr[i]

data = bytearray(data)
data[pos:pos+size] = arr
print(hex(pos))
open('patched', 'wb').write(data)