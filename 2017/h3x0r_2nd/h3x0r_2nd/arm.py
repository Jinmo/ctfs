from itertools import cycle

key = bytearray("314ckC47")
text = bytearray('7b 02 6c 53 39 38 7a 07 64 6e 6d 53 3e 1c 7f 79 03 66 6b 21 5b 16 60 68 72 63 79 1e 0a'.replace(' ', '').decode('hex'))[:-1]
print bytearray([x ^ y for x, y in zip(text, cycle(key))])