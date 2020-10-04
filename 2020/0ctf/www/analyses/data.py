from itertools import cycle
data = open('data', 'rb').read()
key = bytes.fromhex(
    '00 61 73 6D 01 00 00 00 01 62 0F 60 01 7F 01 7F 60 03 7F 7F 7F 01 7F 60 03 7F 7E 7F 01 7E 60 01')
key = key.ljust(0x20, b'\x00')
key = bytearray(key)
key=b'eNj0y_weba5SemB1Y.lstrip("web")!'
arr = list(data)
for j in range(0, len(arr), 512):
    state = 0xff
    for i in range(j, j+512):
        v11 = i & 0x1F
        v7 = key[v11] ^ arr[i] ^ state
        state = arr[i]
        arr[i] = v7-v11&0xff

open('data2', 'wb').write(bytes(arr))
