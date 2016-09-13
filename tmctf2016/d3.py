from itertools import cycle
import requests
from rc4 import RC4
if 0:
	key = '25 29 3D 7E 2A 28 60 3D 24 29 7C 6C 25 29 3D 7E 2A 28 60 3D 24 29 7C 6C'.replace(' ', '').decode('hex')
	data = open('../../../Downloads/tmctf.exe', 'rb').read()
	data = bytearray([ord(x) ^ ord(y) for x, y in zip(data, cycle(key))])
	open('d5.exe', 'wb').write(data)

	Data = [48, 7, 22, 32]
	Key = [0] * 4
	Key[0] = 104
	Key[1] = 117
	Key[2] = 103
	Key[3] = 97

	print bytearray(x ^ y for x, y in zip(Data, Key))

urls = '''4108050209.html
2212294583.html
450215437.html
1842515611.html
4088798008.html
2226203566.html
498629140.html
1790921346.html'''.split('\n')

key = [0] * 100
for i, url in enumerate(urls):
	r = requests.get('http://tmctf2016-03.trendmicro.co.jp/' + url)
	text = bytearray(r.text.decode('base64'))
	if text[0] == 1:
		key[i] = str(text[1:])
	print `text`

key = ''.join(key[1:5])
key2 = bytearray()
key = bytearray(key)
for x, y in zip(RC4(bytearray('tmctf2016-online')), key):
	key2.append(x ^ y)

data = 'F2 40 C2 B3 90 57 A5 E7 54 07 0D D4 B9 8E D4 D1 5C 47 09 5E 1B DF 84 D5 62 47 7D 8D E5'.replace(' ', '').decode('hex')
data = bytearray(data)
result = bytearray()
for x, y in zip(RC4(key2), data):
	result.append(x ^ y)

print result